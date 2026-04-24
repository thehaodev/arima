import streamlit as st

from src.data_utils import load_csv_data, prepare_time_series_dataframe
from src.diagnostics import create_acf_pacf_figures, get_allowed_lag_range
from src.stationarity import apply_differencing, create_time_series_figure


st.title("ARIMA Lab")
st.caption("Tải dữ liệu chuỗi thời gian, quan sát chuỗi gốc và thử sai phân bậc 1 hoặc bậc 2.")

st.info(
    """
    Sai phân giúp chuỗi giảm xu hướng và thường ổn định hơn trước khi đưa vào ARIMA.
    Trong trang này, bạn có thể xem chuỗi gốc rồi so sánh nhanh với chuỗi sau sai phân.
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
        control_col, info_col = st.columns([1, 1])

        with control_col:
            st.subheader("Chọn cột dữ liệu")
            time_column = st.selectbox("Cột thời gian", columns)
            value_options = [column for column in columns if column != time_column]
            value_column = st.selectbox("Cột giá trị", value_options)
            diff_order = st.radio(
                "Mức sai phân",
                options=[0, 1, 2],
                format_func=lambda value: {
                    0: "Chuỗi gốc",
                    1: "Sai phân bậc 1",
                    2: "Sai phân bậc 2",
                }[value],
                horizontal=True,
            )

        with info_col:
            st.subheader("Giải thích ngắn")
            st.write(
                """
                - Chuỗi gốc: dữ liệu ban đầu sau khi đã chuẩn hóa thời gian.
                - Sai phân bậc 1: lấy chênh lệch giữa hai thời điểm liên tiếp.
                - Sai phân bậc 2: sai phân thêm một bước nữa để giảm xu hướng mạnh hơn.
                """
            )
            st.caption("Thường nên bắt đầu từ chuỗi gốc, sau đó mới thử sai phân khi chuỗi còn xu hướng rõ.")

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
