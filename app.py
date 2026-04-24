import streamlit as st


st.set_page_config(
    page_title="ARIMA Learning Web",
    layout="wide",
    initial_sidebar_state="expanded",
)


overview_page = st.Page(
    "page/1_Overview.py",
    title="Overview",
    default=True,
)
theory_page = st.Page(
    "page/2_Theory.py",
    title="Theory",
)
lab_page = st.Page(
    "page/3_ARIMA_Lab.py",
    title="ARIMA Lab",
)
results_page = st.Page(
    "page/4_Results.py",
    title="Results",
)

navigation = st.navigation(
    {
        "ARIMA Learning": [
            overview_page,
            theory_page,
            lab_page,
            results_page,
        ]
    }
)

with st.sidebar:
    st.title("ARIMA Learning Web")
    st.caption("Skeleton multi-page app cho việc học ARIMA.")
    st.divider()
    st.markdown(
        """
        Ứng dụng hiện đang ở giai đoạn khởi tạo:

        - Có điều hướng nhiều trang
        - Có layout và nội dung mẫu
        - Chưa tích hợp logic ARIMA
        """
    )

navigation.run()
