import streamlit as st


st.title("Results")
st.caption("Trang hiển thị kết quả forecast từ ARIMA sau khi chạy trong ARIMA Lab.")

arima_results = st.session_state.get("arima_results")

if not arima_results:
    st.info("Chưa có kết quả ARIMA. Hãy sang trang ARIMA Lab để chọn p, d, q và chạy mô hình.")
else:
    summary_col, metric_col = st.columns([2, 1])

    with summary_col:
        p_value, d_value, q_value = arima_results["order"]
        st.subheader("Tóm tắt kết quả")
        st.write(
            f"""
            Mô hình đã chạy: `ARIMA({p_value}, {d_value}, {q_value})`

            - Cột thời gian: `{arima_results['time_column']}`
            - Cột giá trị: `{arima_results['value_column']}`
            - Forecast trên tập test và forecast tương lai đã được lưu từ ARIMA Lab.
            """
        )

    with metric_col:
        st.subheader("Chỉ số")
        st.metric("MAE", f"{arima_results['mae']:.4f}")
        st.metric("RMSE", f"{arima_results['rmse']:.4f}")

    st.divider()
    st.subheader("Forecast trên test")
    st.dataframe(arima_results["test_forecast_df"], width="stretch")

    st.subheader("Forecast tương lai")
    st.dataframe(arima_results["future_forecast_df"], width="stretch")

    st.caption("Nếu kết quả chưa hợp lý, hãy quay lại ARIMA Lab để đổi p, d, q hoặc cách chia train/test.")
