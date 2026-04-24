import streamlit as st


st.title("Results")
st.caption("Trang hiển thị kết quả mô hình và diễn giải. Hiện tại là placeholder.")

summary_col, metric_col = st.columns([2, 1])

with summary_col:
    st.subheader("Tóm tắt kết quả")
    st.write(
        """
        Khu vực này sẽ hiển thị thông tin tổng quan sau khi chạy mô hình:
        tham số đã chọn, trạng thái chạy, và nhận xét ngắn về đầu ra.
        """
    )
    st.info("Placeholder: chưa có kết quả thật vì chưa tích hợp pipeline ARIMA.")

with metric_col:
    st.subheader("Chỉ số")
    st.metric("AIC", "--")
    st.metric("BIC", "--")
    st.metric("RMSE", "--")

st.divider()

chart_col, notes_col = st.columns([3, 2])

with chart_col:
    st.subheader("Biểu đồ")
    st.empty()
    st.caption("Placeholder cho biểu đồ chuỗi gốc, fitted values hoặc forecast.")

with notes_col:
    st.subheader("Diễn giải")
    st.write(
        """
        Phần này sẽ giải thích kết quả theo ngôn ngữ đơn giản:
        mô hình đang làm gì, kết quả có hợp lý không, và cần thử điều chỉnh gì tiếp theo.
        """
    )

st.warning("Trang kết quả hiện chưa kết nối với dữ liệu hoặc mô hình thực tế.")
