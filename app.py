import streamlit as st


st.set_page_config(
    page_title="ARIMA Demo Lab",
    layout="wide",
    initial_sidebar_state="expanded",
)


lab_page = st.Page(
    "page/3_ARIMA_Lab.py",
    title="ARIMA Lab",
    default=True,
)

navigation = st.navigation({"Demo": [lab_page]})

with st.sidebar:
    st.title("ARIMA Demo Lab")
    st.caption("Một luồng demo trực quan để thử ARIMA trên dữ liệu chuỗi thời gian.")
    st.divider()
    st.markdown(
        """
        Các bước:

        1. Chọn sample dataset hoặc tải lên file CSV
        2. Quan sát chuỗi gốc
        3. Thử differencing và kiểm tra tính dừng
        4. Xem ACF/PACF
        5. Chọn `p, d, q` và fit ARIMA
        6. Xem forecast, residual và metrics ngay trong cùng trang
        """
    )

navigation.run()
