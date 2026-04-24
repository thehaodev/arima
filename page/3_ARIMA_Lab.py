import streamlit as st


st.title("ARIMA Lab")
st.caption("Không gian thực hành ARIMA. Hiện tại mới có layout placeholder.")

left_col, right_col = st.columns([1, 1])

with left_col:
    st.subheader("Dữ liệu đầu vào")
    st.file_uploader("Tải file CSV", type=["csv"], disabled=True)
    st.selectbox("Chọn cột thời gian", ["Chưa có dữ liệu"], disabled=True)
    st.selectbox("Chọn cột giá trị", ["Chưa có dữ liệu"], disabled=True)
    st.info("Placeholder: chức năng upload, preview và chọn cột sẽ được thêm sau.")

with right_col:
    st.subheader("Cấu hình mô hình")
    st.number_input("p", min_value=0, value=0, disabled=True)
    st.number_input("d", min_value=0, value=0, disabled=True)
    st.number_input("q", min_value=0, value=0, disabled=True)
    st.button("Chạy ARIMA", disabled=True)
    st.info("Placeholder: chưa có logic huấn luyện hoặc dự báo.")

st.divider()

st.subheader("Xem trước dữ liệu")
st.dataframe(
    [
        {"time": "YYYY-MM-DD", "value": "..."},
        {"time": "YYYY-MM-DD", "value": "..."},
        {"time": "YYYY-MM-DD", "value": "..."},
    ],
    use_container_width=True,
)

st.caption("Bảng trên chỉ là dữ liệu mẫu để thể hiện bố cục giao diện.")
