import streamlit as st


st.title("Theory")
st.caption("Tổng hợp các khái niệm nền tảng cần biết trước khi học ARIMA.")

sections = [
    (
        "Time Series",
        "Chuỗi thời gian là tập dữ liệu được sắp xếp theo thứ tự thời gian, ví dụ doanh số theo tháng hoặc nhiệt độ theo ngày.",
    ),
    (
        "Stationarity",
        "Tính dừng mô tả chuỗi có đặc trưng thống kê ổn định theo thời gian, như trung bình và phương sai không thay đổi quá mạnh.",
    ),
    (
        "Differencing",
        "Sai phân là cách lấy hiệu giữa các giá trị liên tiếp để giảm xu hướng và giúp chuỗi tiến gần hơn tới trạng thái dừng.",
    ),
    (
        "AR",
        "Thành phần AutoRegressive mô tả việc giá trị hiện tại phụ thuộc vào các giá trị trong quá khứ của chính chuỗi.",
    ),
    (
        "MA",
        "Thành phần Moving Average mô tả ảnh hưởng của sai số trong quá khứ lên giá trị hiện tại của chuỗi.",
    ),
    (
        "ACF/PACF",
        "ACF và PACF hỗ trợ quan sát độ tương quan theo độ trễ, từ đó gợi ý cách chọn tham số ban đầu cho mô hình.",
    ),
    (
        "ARIMA",
        "ARIMA kết hợp AR, I và MA để mô hình hóa chuỗi thời gian sau khi đã xử lý phù hợp, thường dùng cho dự báo ngắn hạn.",
    ),
]

for title, description in sections:
    st.subheader(title)
    st.write(description)
    st.info(
        "Placeholder: phần này sẽ được mở rộng bằng ví dụ, hình minh họa hoặc công thức ở các bước sau."
    )

st.divider()
st.warning("Trang này hiện chỉ là nội dung khung, chưa có biểu đồ, công thức chi tiết hoặc tương tác.")
