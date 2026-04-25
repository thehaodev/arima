import streamlit as st

from src.app_state import clear_arima_results, get_arima_results, save_arima_results
from src.data_utils import (
    load_csv_sample,
    load_sample_csv_data,
    prepare_time_series_dataframe,
    read_csv_columns,
)
from src.diagnostics import create_acf_figure, create_acf_pacf_figures, get_allowed_lag_range
from src.modeling import fit_arima_workflow
from src.plotting import create_multi_line_figure
from src.stationarity import (
    apply_differencing,
    create_time_series_figure,
    run_adf_test,
    suggest_d_order,
)


PLACEHOLDER_PREVIEW = [
    {"time": "YYYY-MM-DD", "value": "..."},
    {"time": "YYYY-MM-DD", "value": "..."},
    {"time": "YYYY-MM-DD", "value": "..."},
]
SUGGESTED_D_KEY = "suggested_d_result"
SUGGESTED_D_TRACE_KEY = "suggested_d_trace"
SELECTED_DIFF_ORDER_KEY = "selected_diff_order"


def render_chart(dataframe, time_column: str, value_column: str, title: str) -> None:
    """Render a time-series chart with graceful error handling."""
    try:
        figure = create_time_series_figure(
            dataframe,
            time_column=time_column,
            value_column=value_column,
            title=title,
        )
    except ValueError as error:
        st.error(str(error))
    else:
        st.plotly_chart(figure, width="stretch")


def render_preview(dataframe, caption: str) -> None:
    """Render a compact dataframe preview."""
    st.dataframe(dataframe.head(20), width="stretch")
    st.caption(caption)


def load_selected_dataset(source: str) -> tuple[object | None, str | None]:
    """Load the bundled sample dataset only."""
    if source == "Dùng sample dataset":
        return load_sample_csv_data(), "sample_series.csv"
    return None, None


def get_default_column_index(columns: list[str], candidates: list[str]) -> int:
    """Return the first matching column index from candidate names."""
    lowered_columns = [column.lower() for column in columns]
    for candidate in candidates:
        if candidate in lowered_columns:
            return lowered_columns.index(candidate)
    return 0


def render_adf_result(title: str, result: dict) -> None:
    """Render a compact ADF summary."""
    st.markdown(f"**{title}**")
    metric_col1, metric_col2 = st.columns(2)
    metric_col1.metric("ADF statistic", f"{result['statistic']:.4f}")
    metric_col2.metric("p-value", f"{result['p_value']:.4f}")
    st.caption(result["decision"])


def render_adf_section(original_series_df, differenced_df, value_column: str) -> None:
    """Render ADF tests for the original and selected differenced series."""
    st.subheader("Kiểm tra ADF")
    st.caption(
        "p-value nhỏ: có bằng chứng mạnh hơn để xem chuỗi là dừng. p-value lớn: chưa có đủ bằng chứng để xem chuỗi là dừng."
    )

    left_col, right_col = st.columns(2)
    try:
        original_adf = run_adf_test(original_series_df, value_column)
    except ValueError as error:
        left_col.warning(str(error))
    else:
        with left_col:
            render_adf_result("Chuỗi gốc", original_adf)

    try:
        differenced_adf = run_adf_test(differenced_df, value_column)
    except ValueError as error:
        right_col.warning(str(error))
    else:
        with right_col:
            render_adf_result("Chuỗi đang chọn", differenced_adf)


def render_suggest_d_section(prepared_df, time_column: str, value_column: str) -> None:
    """Render the d suggestion action and trace table."""
    action_col, info_col = st.columns([1, 2])
    with action_col:
        if st.button("Gợi ý d"):
            try:
                suggested_d, trace_df = suggest_d_order(
                    prepared_df,
                    time_column=time_column,
                    value_column=value_column,
                )
            except ValueError as error:
                st.warning(str(error))
            else:
                st.session_state[SUGGESTED_D_KEY] = suggested_d
                st.session_state[SUGGESTED_D_TRACE_KEY] = trace_df
                st.session_state[SELECTED_DIFF_ORDER_KEY] = suggested_d

    suggested_d = st.session_state.get(SUGGESTED_D_KEY)
    trace_df = st.session_state.get(SUGGESTED_D_TRACE_KEY)

    with info_col:
        if suggested_d is not None:
            st.info(f"Gợi ý d: `{suggested_d}`. Bạn có thể chỉnh tay ở mục chọn d ngay bên dưới.")

    if trace_df is not None:
        st.dataframe(trace_df, width="stretch")


def render_acf_pacf_section(dataframe, value_column: str) -> None:
    """Render ACF/PACF controls and charts."""
    st.subheader("4. ACF/PACF")
    st.caption(
        "Nên đọc ACF/PACF trên chuỗi đã được làm dừng. PACF thường gợi ý `p` ban đầu, còn ACF thường gợi ý `q` ban đầu."
    )

    try:
        min_lag, max_lag = get_allowed_lag_range(len(dataframe))
    except ValueError as error:
        st.warning(str(error))
        return

    lag_count = st.slider(
        "Chọn số lag",
        min_value=min_lag,
        max_value=max_lag,
        value=min(10, max_lag),
    )

    try:
        acf_figure, pacf_figure = create_acf_pacf_figures(
            dataframe,
            value_column=value_column,
            lags=lag_count,
        )
    except ValueError as error:
        st.warning(str(error))
        return

    acf_col, pacf_col = st.columns(2)
    with acf_col:
        st.plotly_chart(acf_figure, width="stretch")
    with pacf_col:
        st.plotly_chart(pacf_figure, width="stretch")


def render_saved_results() -> None:
    """Render persisted ARIMA results at the end of the page."""
    arima_results = get_arima_results()
    if not arima_results:
        st.info("Chưa có kết quả forecast. Hãy chọn tham số và bấm `Chạy ARIMA`.")
        return

    p_value, d_value, q_value = arima_results["order"]
    st.markdown(f"**Mô hình hiện tại: `ARIMA({p_value},{d_value},{q_value})`**")

    metric_col1, metric_col2 = st.columns(2)
    metric_col1.metric("MAE", f"{arima_results['mae']:.4f}")
    metric_col2.metric("RMSE", f"{arima_results['rmse']:.4f}")

    st.subheader("Giá trị thực tế và forecast")
    try:
        forecast_figure = create_multi_line_figure(
            [
                {
                    "x": arima_results["test_forecast_df"][arima_results["time_column"]],
                    "y": arima_results["test_forecast_df"]["actual"],
                    "name": "Thực tế",
                },
                {
                    "x": arima_results["test_forecast_df"][arima_results["time_column"]],
                    "y": arima_results["test_forecast_df"]["forecast"],
                    "name": "Forecast",
                },
            ],
            title="Thực tế và forecast trên tập test",
            xaxis_title=arima_results["time_column"],
            yaxis_title=arima_results["value_column"],
        )
    except ValueError as error:
        st.warning(str(error))
    else:
        st.plotly_chart(forecast_figure, width="stretch")

    st.subheader("Forecast trên tập test")
    st.dataframe(arima_results["test_forecast_df"], width="stretch")

    st.subheader("Chẩn đoán residual")
    st.caption("Residual dao động quanh 0 và chưa thấy tự tương quan đáng kể thường là dấu hiệu tốt hơn.")
    summary_col1, summary_col2, summary_col3 = st.columns(3)
    summary_col1.metric("Trung bình residual", f"{arima_results['residual_summary']['mean']:.4f}")
    summary_col2.metric("Độ lệch chuẩn residual", f"{arima_results['residual_summary']['std']:.4f}")
    summary_col3.metric("Ljung-Box p-value", f"{arima_results['ljung_box_pvalue']:.4f}")
    st.caption(
        "p-value Ljung-Box lớn hơn thường cho thấy chưa có bằng chứng mạnh về tự tương quan đáng kể trong residual."
    )

    try:
        residual_figure = create_multi_line_figure(
            [
                {
                    "x": arima_results["residual_df"][arima_results["time_column"]],
                    "y": arima_results["residual_df"]["residual"],
                    "name": "Residual",
                }
            ],
            title="Residual trên chuỗi dùng để fit mô hình",
            xaxis_title=arima_results["time_column"],
            yaxis_title="Residual",
        )
    except ValueError as error:
        st.warning(str(error))
    else:
        st.plotly_chart(residual_figure, width="stretch")

    try:
        residual_acf_figure = create_acf_figure(
            arima_results["residual_df"],
            value_column="residual",
            lags=10,
            title="ACF của residual",
        )
    except ValueError as error:
        st.warning(str(error))
    else:
        st.plotly_chart(residual_acf_figure, width="stretch")

    st.dataframe(arima_results["residual_df"].head(20), width="stretch")

    st.subheader("Forecast tương lai")
    st.dataframe(arima_results["future_forecast_df"], width="stretch")


def sync_results_with_current_selection(dataset_name: str, time_column: str, value_column: str) -> None:
    """Clear saved results if the current dataset selection has changed."""
    arima_results = get_arima_results()
    should_clear = False
    if arima_results and (
        arima_results.get("dataset_name") != dataset_name
        or arima_results.get("time_column") != time_column
        or arima_results.get("value_column") != value_column
    ):
        should_clear = True

    if should_clear:
        clear_arima_results()
        st.session_state.pop(SUGGESTED_D_KEY, None)
        st.session_state.pop(SUGGESTED_D_TRACE_KEY, None)
        st.session_state.pop(SELECTED_DIFF_ORDER_KEY, None)


def render_modeling_section(prepared_df, time_column: str, value_column: str, default_d: int) -> None:
    """Render ARIMA controls and persist results to session state."""
    st.subheader("5. Chọn p, d, q và fit ARIMA")
    st.caption("Giữ UI đơn giản: tự chọn tham số, chia train/test, rồi xem forecast ngay bên dưới.")
    st.markdown(
        """
        - `p`: số độ trễ của phần AR
        - `d`: bậc sai phân
        - `q`: số độ trễ của phần MA
        """
    )

    model_col, config_col = st.columns([1, 1])
    with model_col:
        p_value = st.number_input("p", min_value=0, max_value=5, value=1, step=1)
        d_value = st.number_input("d", min_value=0, max_value=2, value=default_d, step=1)
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

    st.markdown(f"**Mô hình đang chuẩn bị fit: `ARIMA({p_value},{d_value},{q_value})`**")

    if not st.button("Chạy ARIMA", type="primary"):
        return

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
        clear_arima_results()
        st.error(str(error))
        return

    save_arima_results(
        dataset_name=st.session_state.get("selected_dataset_name", ""),
        time_column=time_column,
        value_column=value_column,
        order=arima_results["order"],
        mae=arima_results["mae"],
        rmse=arima_results["rmse"],
        test_forecast_df=arima_results["test_forecast_df"],
        future_forecast_df=arima_results["future_forecast_df"],
        residual_df=arima_results["residual_df"],
        residual_summary=arima_results["residual_summary"],
        ljung_box_pvalue=arima_results["ljung_box_pvalue"],
    )

    p_value, d_value, q_value = arima_results["order"]
    st.success(f"Fit ARIMA thành công với mô hình `ARIMA({p_value},{d_value},{q_value})`. Kết quả được hiển thị ngay bên dưới.")


def main() -> None:
    """Render the single-page ARIMA demo flow."""
    st.title("ARIMA Lab")
    st.caption("Một trang demo trực quan để đi từ dữ liệu đầu vào đến forecast và metrics.")

    st.subheader("1. Chọn dữ liệu")
    st.caption("Bạn có thể dùng sample dataset đi kèm để demo nhanh, hoặc tải lên CSV riêng.")

    source = st.radio(
        "Nguồn dữ liệu",
        options=["Dùng sample dataset", "Tải lên CSV riêng"],
        horizontal=True,
    )
    uploaded_file = None
    if source == "Tải lên CSV riêng":
        uploaded_file = st.file_uploader("Tải file CSV", type=["csv"])

    try:
        raw_df, dataset_name = load_selected_dataset(source)
    except ValueError as error:
        clear_arima_results()
        st.error(str(error))
        return

    if raw_df is None:
        if uploaded_file is None:
            clear_arima_results()
            st.dataframe(PLACEHOLDER_PREVIEW, width="stretch")
            st.caption("Chưa có dữ liệu. Hãy tải lên một file CSV để tiếp tục.")
            return

        try:
            columns = read_csv_columns(uploaded_file)
        except ValueError as error:
            clear_arima_results()
            st.error(str(error))
            return

        dataset_name = uploaded_file.name
        st.session_state["selected_dataset_name"] = dataset_name
        st.success(f"Đang dùng dữ liệu: `{dataset_name}`")

        select_col, info_col = st.columns([1, 1])
        default_time_index = get_default_column_index(columns, ["date", "time", "timestamp", "datetime"])
        default_value_index = get_default_column_index(columns, ["value", "sales", "close", "y"])
        if default_value_index == default_time_index:
            default_value_index = 0 if len(columns) == 1 else (1 if default_time_index == 0 else 0)

        with select_col:
            time_column = st.selectbox("Cột thời gian", columns, index=default_time_index)
            value_options = [column for column in columns if column != time_column]
            value_column = st.selectbox(
                "Cột giá trị",
                value_options,
                index=min(default_value_index, len(value_options) - 1),
            )
            sample_size = st.number_input(
                "Số sample để load",
                min_value=100,
                max_value=100000,
                value=5000,
                step=100,
            )

        with info_col:
            st.write(
                """
                Với file CSV nặng, app sẽ:
                - chỉ đọc header trước để chọn cột
                - sau đó chỉ load 2 cột đã chọn
                - và chỉ load đúng số sample bạn chọn
                """
            )

        try:
            raw_df = load_csv_sample(
                uploaded_file,
                time_column=time_column,
                value_column=value_column,
                sample_size=int(sample_size),
            )
        except ValueError as error:
            clear_arima_results()
            st.error(str(error))
            return
    else:
        st.session_state["selected_dataset_name"] = dataset_name
        st.success(f"Đang dùng dữ liệu: `{dataset_name}`")

        columns = raw_df.columns.tolist()
        select_col, info_col = st.columns([1, 1])
        default_time_index = get_default_column_index(columns, ["date", "time", "timestamp", "datetime"])
        default_value_index = get_default_column_index(columns, ["value", "sales", "close", "y"])
        if default_value_index == default_time_index:
            default_value_index = 0 if len(columns) == 1 else (1 if default_time_index == 0 else 0)

        with select_col:
            time_column = st.selectbox("Cột thời gian", columns, index=default_time_index)
            value_options = [column for column in columns if column != time_column]
            value_column = st.selectbox(
                "Cột giá trị",
                value_options,
                index=min(default_value_index, len(value_options) - 1),
            )

        with info_col:
            st.write(
                """
                Dữ liệu sẽ được:
                - chuyển cột thời gian sang `datetime`
                - sắp xếp tăng dần theo thời gian
                - giữ lại đúng 2 cột đang chọn để demo ARIMA
                """
            )

    sync_results_with_current_selection(dataset_name, time_column, value_column)

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
    except ValueError as error:
        clear_arima_results()
        st.error(str(error))
        return

    st.divider()
    st.subheader("2. Quan sát chuỗi gốc")
    st.caption("Nhìn nhanh xu hướng và độ dao động trước khi thử sai phân.")
    render_chart(original_series_df, time_column, value_column, "Chuỗi thời gian gốc")
    render_preview(
        original_series_df,
        "Preview dữ liệu gốc sau khi chuẩn hóa cột thời gian và sắp xếp theo thời gian.",
    )

    st.divider()
    st.subheader("3. Differencing")
    st.caption("d = 0: chưa sai phân. d = 1: sai phân bậc 1. d = 2: sai phân bậc 2.")
    render_suggest_d_section(prepared_df, time_column, value_column)

    if SELECTED_DIFF_ORDER_KEY not in st.session_state:
        st.session_state[SELECTED_DIFF_ORDER_KEY] = 0

    diff_order = st.radio(
        "Mức sai phân để quan sát",
        options=[0, 1, 2],
        format_func=lambda value: {
            0: "d = 0: chưa sai phân",
            1: "d = 1: sai phân bậc 1",
            2: "d = 2: sai phân bậc 2",
        }[value],
        horizontal=True,
        key=SELECTED_DIFF_ORDER_KEY,
    )

    try:
        differenced_df = apply_differencing(
            prepared_df,
            time_column=time_column,
            value_column=value_column,
            order=diff_order,
        )
    except ValueError as error:
        clear_arima_results()
        st.error(str(error))
        return

    diff_title = {
        0: "Chuỗi hiện đang xem",
        1: "Chuỗi sau sai phân bậc 1",
        2: "Chuỗi sau sai phân bậc 2",
    }[diff_order]
    render_chart(differenced_df, time_column, value_column, diff_title)
    render_preview(differenced_df, "Preview dữ liệu sau sai phân để dùng cho phần quan sát ACF/PACF.")
    render_adf_section(original_series_df, differenced_df, value_column)

    st.divider()
    render_acf_pacf_section(differenced_df, value_column)

    st.divider()
    render_modeling_section(prepared_df, time_column, value_column, diff_order)

    st.divider()
    st.subheader("6. Forecast và metrics")
    st.caption("Kết quả được gom ngay cuối trang để thuận tiện demo trực quan.")
    render_saved_results()


main()
