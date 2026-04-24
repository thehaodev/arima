import streamlit as st


st.title("Overview")
st.caption("Trang giới thiệu tổng quan về project ARIMA learning web.")

st.markdown(
    """
    Ứng dụng này được xây dựng để hỗ trợ học ARIMA theo từng bước:
    từ khái niệm nền tảng, thực hành trên dữ liệu, đến xem kết quả đầu ra.
    """
)

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Mục tiêu")
    st.write(
        """
        - Giải thích các khái niệm chính của chuỗi thời gian.
        - Tạo không gian thực hành ARIMA đơn giản, dễ theo dõi.
        - Trình bày kết quả theo hướng học tập, không quá kỹ thuật.
        """
    )

with col2:
    st.subheader("Trạng thái hiện tại")
    st.info("Đây là skeleton UI. Chưa có xử lý dữ liệu và chưa có mô hình ARIMA.")

st.divider()

st.subheader("Luồng học dự kiến")
st.write(
    """
    1. Đọc phần Overview để hiểu cấu trúc ứng dụng.
    2. Sang Theory để xem các khái niệm nền tảng.
    3. Mở ARIMA Lab để thao tác với dữ liệu và cấu hình mô hình.
    4. Xem Results để đọc kết quả và diễn giải.
    """
)

st.subheader("Các trang trong ứng dụng")
pages = st.columns(4)

pages[0].metric("Overview", "Sẵn sàng", help="Trang giới thiệu tổng quan.")
pages[1].metric("Theory", "Sẵn sàng", help="Trang tóm tắt kiến thức nền.")
pages[2].metric("ARIMA Lab", "Placeholder", help="Trang thực hành sẽ làm sau.")
pages[3].metric("Results", "Placeholder", help="Trang kết quả sẽ làm sau.")
