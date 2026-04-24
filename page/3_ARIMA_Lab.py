import streamlit as st

from src.data_utils import load_csv_data, prepare_time_series_dataframe
from src.diagnostics import create_acf_pacf_figures, get_allowed_lag_range
from src.modeling import fit_arima_workflow
from src.stationarity import apply_differencing, create_time_series_figure


st.title("ARIMA Lab")
st.caption("Tải dữ liệu chuỗi thời gian, quan sát chuỗi, thử sai phân và fit ARIMA theo tham số tự chọn.")

st.info(
    """
    Quy trình tối thiểu trong trang này:
    1. Tải CSV và chọn cột thời gian, cột giá trị.
    2. Quan sát chuỗi gốc và chuỗi sau sai phân.
    3. Xem ACF/PACF để gợi ý p và q ban đầu.
    4. Chọn p, d, q rồi chạy ARIMA để forecast.
    """
)

uploaded_file = st.file_uploader("Tải file CSV", type=["csv"])

if uploaded_file is None:
    st.info("Hãy tải lên một file CSV để bắt đầu.")
    st.subheader("Xem trước dữ liệu")
    st.dataframe(
        [
            {"time": "YYYY-MM-DD", "value": "..."},
            {"time": "YYYY-MM-DD", "value": "..."},
            {"time": "YYYY-MM-DD", "value": "..."},
        ],
        width="stretch",
    )
else:
    try:
        raw_df = load_csv_data(uploaded_file)
    except ValueError as error:
        st.error(str(error))
    else:
        columns = raw_df.columns.tolist()
        top_left_col, top_right_col = st.columns([1, 1])

        with top_left_col:
            st.subheader("Chọn cột dữ liệu")
            time_column = st.selectbox("Cột thời gian", columns)
            value_options = [column for column in columns if column != time_column]
            value_column = st.selectbox("Cột giá trị", value_options)
            diff_order = st.radio(
                "Mức sai phân để quan sát",
                options=[0, 1, 2],
                format_func=lambda value: {
                    0: "Chuỗi gốc",
                    1: "Sai phân bậc 1",
                    2: "Sai phân bậc 2",
                }[value],
                horizontal=True,
            )

        with top_right_col:
            st.subheader("Giải thích ngắn")
            st.write(
                """
                - Chuỗi gốc: dữ liệu ban đầu sau khi chuẩn hóa thời gian.
                - Sai phân bậc 1: lấy chênh lệch giữa hai thời điểm liên tiếp.
                - Sai phân bậc 2: sai phân thêm một lần nữa để giảm xu hướng mạnh hơn.
                """
            )
            st.caption("Sai phân ở đây chỉ để quan sát. Khi fit ARIMA, bạn vẫn tự chọn tham số `d` riêng.")

        try:
            prepared_df = prepare_time_series_dataframe(
                raw_df,
                time_column=time_column,
                value_column=value_column,
            )
            original_series_df = apply_differencing(
                prepared_df,
                time_column=time_column,
                value_column=value_column,
                order=0,
            )
            differenced_df = apply_differencing(
                prepared_df,
                time_column=time_column,
                value_column=value_column,
                order=diff_order,
            )
        except ValueError as error:
            st.error(str(error))
        else:
            st.divider()
            st.subheader("Biểu đồ chuỗi thời gian gốc")

            try:
                original_figure = create_time_series_figure(
                    original_series_df,
                    time_column=time_column,
                    value_column=value_column,
                    title="Chuỗi thời gian gốc",
                )
            except ValueError as error:
                st.error(str(error))
            else:
                st.plotly_chart(original_figure, width="stretch")

            st.subheader("Xem trước dữ liệu gốc")
            st.dataframe(original_series_df.head(20), width="stretch")

            st.divider()
            section_title = {
                0: "Chuỗi hiện đang xem",
                1: "Chuỗi sau sai phân bậc 1",
                2: "Chuỗi sau sai phân bậc 2",
            }[diff_order]
            st.subheader(section_title)

            try:
                differenced_figure = create_time_series_figure(
                    differenced_df,
                    time_column=time_column,
                    value_column=value_column,
                    title=section_title,
                )
            except ValueError as error:
                st.error(str(error))
            else:
                st.plotly_chart(differenced_figure, width="stretch")

            st.dataframe(differenced_df.head(20), width="stretch")
            st.caption("Preview hiển thị dữ liệu sau khi convert thời gian, sort theo thời gian và áp dụng sai phân nếu có.")

            st.divider()
            st.subheader("ACF và PACF")
            st.write(
                """
                ACF và PACF là hai biểu đồ hỗ trợ chọn tham số ban đầu cho ARIMA.
                Hiểu nhanh:
                - ACF thường dùng để gợi ý `q`
                - PACF thường dùng để gợi ý `p`
                """
            )

            try:
                min_lag, max_lag = get_allowed_lag_range(len(differenced_df))
            except ValueError as error:
                st.warning(str(error))
            else:
                lag_count = st.slider(
                    "Chọn số lag",
                    min_value=min_lag,
                    max_value=max_lag,
                    value=min(10, max_lag),
                )

                try:
                    acf_figure, pacf_figure = create_acf_pacf_figures(
                        differenced_df,
                        value_column=value_column,
                        lags=lag_count,
                    )
                except ValueError as error:
                    st.warning(str(error))
                else:
                    acf_col, pacf_col = st.columns(2)
                    with acf_col:
                        st.plotly_chart(acf_figure, width="stretch")
                    with pacf_col:
                        st.plotly_chart(pacf_figure, width="stretch")

            st.divider()
            st.subheader("Fit ARIMA")
            st.write("Chọn `p, d, q`, chia train/test, forecast trên test và forecast tương lai.")

            model_col, config_col = st.columns([1, 1])
            with model_col:
                p_value = st.number_input("p", min_value=0, max_value=5, value=1, step=1)
                d_value = st.number_input("d", min_value=0, max_value=2, value=diff_order, step=1)
                q_value = st.number_input("q", min_value=0, max_value=5, value=1, step=1)

            with config_col:
                max_test_size = max(1, min(20, len(prepared_df) - 2))
                test_size = st.slider(
                    "Số điểm test",
                    min_value=1,
                    max_value=max_test_size,
                    value=min(5, max_test_size),
                )
                future_steps = st.number_input(
                    "Số bước forecast tương lai",
                    min_value=1,
                    max_value=30,
                    value=5,
                    step=1,
                )

            if st.button("Chạy ARIMA"):
                try:
                    arima_results = fit_arima_workflow(
                        prepared_df,
                        time_column=time_column,
                        value_column=value_column,
                        order=(p_value, d_value, q_value),
                        test_size=test_size,
                        future_steps=future_steps,
                    )
                except ValueError as error:
                    st.error(str(error))
                    st.session_state.pop("arima_results", None)
                else:
                    st.session_state["arima_results"] = {
                        "time_column": time_column,
                        "value_column": value_column,
                        "order": arima_results["order"],
                        "mae": arima_results["mae"],
                        "rmse": arima_results["rmse"],
                        "test_forecast_df": arima_results["test_forecast_df"],
                        "future_forecast_df": arima_results["future_forecast_df"],
                    }

                    metric_col1, metric_col2 = st.columns(2)
                    metric_col1.metric("MAE", f"{arima_results['mae']:.4f}")
                    metric_col2.metric("RMSE", f"{arima_results['rmse']:.4f}")

                    st.subheader("Forecast trên test")
                    st.dataframe(arima_results["test_forecast_df"], width="stretch")

                    st.subheader("Forecast tương lai")
                    st.dataframe(arima_results["future_forecast_df"], width="stretch")

                    st.success("Đã lưu bảng forecast sang trang Results.")
