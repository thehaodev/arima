import streamlit as st


st.title("Lý thuyết ARIMA")
st.caption("Tổng hợp các khái niệm nền tảng để hiểu mô hình ARIMA theo cách dễ đọc, dễ theo dõi.")

st.markdown(
    """
    ARIMA không phải là một công cụ "đoán tương lai" một cách kỳ diệu.
    Nó là một cách nhìn có cấu trúc vào dữ liệu theo thời gian:
    chuỗi đã đi như thế nào trong quá khứ, mức độ ổn định ra sao,
    và phần nào của quá khứ đang ảnh hưởng tới hiện tại.
    """
)

st.divider()

st.subheader("Chuỗi thời gian")
st.write(
    """
    Chuỗi thời gian là dữ liệu được sắp theo thứ tự thời gian.
    Ví dụ quen thuộc là doanh số theo tháng, số người dùng theo ngày,
    giá cổ phiếu theo giờ, hoặc nhiệt độ theo từng ngày.

    Điểm khác biệt lớn nhất của chuỗi thời gian là thứ tự của dữ liệu rất quan trọng.
    Ta không chỉ quan tâm giá trị lớn hay nhỏ, mà còn quan tâm nó xảy ra khi nào
    và có liên hệ gì với các mốc thời gian trước đó.
    """
)

with st.expander("Ví dụ dễ hình dung"):
    st.write(
        """
        Nếu doanh số tháng 1, 2, 3 lần lượt là 100, 120, 140 thì ta thấy có xu hướng tăng.
        Nhưng nếu chỉ nhìn ba con số này mà bỏ thứ tự thời gian, ta sẽ mất thông tin quan trọng nhất:
        dữ liệu đang thay đổi theo thời gian như thế nào.
        """
    )

st.divider()

st.subheader("Stationarity")
st.write(
    """
    Stationarity, hay tính dừng, là ý tưởng rằng đặc tính chung của chuỗi
    không thay đổi quá mạnh theo thời gian.

    Nói đơn giản hơn, nếu một chuỗi là dừng thì:
    - mức trung bình của nó không trôi đi quá xa,
    - độ dao động không phình to hoặc co lại bất thường,
    - cách các điểm dữ liệu liên hệ với nhau khá ổn định.

    Đây là khái niệm rất quan trọng vì ARIMA thường hoạt động tốt hơn
    khi chuỗi đã gần với trạng thái dừng.
    """
)

with st.expander("Dấu hiệu một chuỗi có thể chưa dừng"):
    st.write(
        """
        - Có xu hướng tăng hoặc giảm rõ rệt theo thời gian.
        - Biên độ dao động thay đổi mạnh giữa các giai đoạn.
        - Có mùa vụ lặp lại rõ ràng mà chưa được xử lý.
        """
    )

st.divider()

st.subheader("Differencing")
st.write(
    """
    Differencing, hay sai phân, là cách lấy hiệu giữa các giá trị liên tiếp.
    Mục tiêu là làm cho chuỗi bớt xu hướng hơn và tiến gần tới tính dừng.

    Ví dụ:
    nếu chuỗi gốc là 100, 120, 140, 160
    thì sai phân bậc 1 sẽ là 20, 20, 20.

    Khi đó, thay vì nhìn trực tiếp vào mức giá trị ban đầu,
    ta nhìn vào mức thay đổi giữa các thời điểm.
    """
)

with st.expander("Hiểu nhanh về bậc sai phân d"):
    st.write(
        """
        - `d = 0`: không sai phân, dùng chuỗi gốc.
        - `d = 1`: lấy sai phân một lần.
        - `d = 2`: lấy sai phân hai lần nếu chuỗi vẫn chưa đủ ổn định.

        Trong thực tế, thường ưu tiên giá trị `d` nhỏ để mô hình đơn giản và dễ diễn giải hơn.
        """
    )

st.divider()

st.subheader("AR")
st.write(
    """
    AR là viết tắt của AutoRegressive.
    Ý tưởng của phần AR là giá trị hiện tại có thể phụ thuộc vào chính các giá trị trước đó.

    Nói cách khác, quá khứ của chuỗi có "ký ức" và ký ức đó giúp giải thích hiện tại.
    Nếu hôm nay chịu ảnh hưởng mạnh từ vài ngày trước, thành phần AR có thể mô tả điều này.
    """
)

with st.expander("Hiểu nhanh tham số p"):
    st.write(
        """
        Tham số `p` cho biết mô hình nhìn lại bao nhiêu bước quá khứ
        trong phần AutoRegressive.

        Ví dụ:
        - `p = 1`: nhìn 1 bước trước
        - `p = 2`: nhìn 2 bước trước
        """
    )

st.divider()

st.subheader("MA")
st.write(
    """
    MA là viết tắt của Moving Average.
    Trong ARIMA, MA không mang nghĩa "đường trung bình trượt" như cách gọi quen thuộc trong trực quan hóa.

    Ở đây, MA mô tả việc giá trị hiện tại chịu ảnh hưởng từ sai số trong quá khứ.
    Nếu ở những thời điểm trước mô hình dự đoán lệch nhiều,
    thì thông tin về các sai số đó có thể giúp điều chỉnh dự báo hiện tại.
    """
)

with st.expander("Hiểu nhanh tham số q"):
    st.write(
        """
        Tham số `q` cho biết mô hình dùng bao nhiêu bước sai số quá khứ
        trong phần Moving Average.

        Có thể hiểu đơn giản:
        AR nhìn vào giá trị quá khứ,
        còn MA nhìn vào lỗi dự đoán trong quá khứ.
        """
    )

st.divider()

st.subheader("ACF/PACF")
st.write(
    """
    ACF và PACF là hai công cụ thường dùng để quan sát mối liên hệ theo độ trễ.
    Chúng không trực tiếp tạo ra mô hình, nhưng rất hữu ích khi chọn tham số ban đầu.
    """
)

col1, col2 = st.columns(2)

with col1:
    st.markdown("**ACF**")
    st.write(
        """
        ACF cho thấy mức tương quan giữa chuỗi hiện tại và các giá trị trễ trước đó.
        Nó giúp ta nhìn xem ảnh hưởng của quá khứ kéo dài tới đâu.
        """
    )

with col2:
    st.markdown("**PACF**")
    st.write(
        """
        PACF tập trung vào tương quan trực tiếp tại từng độ trễ,
        sau khi đã loại bớt ảnh hưởng gián tiếp từ các độ trễ khác.
        """
    )

with st.expander("Dùng ACF/PACF để làm gì trong thực hành"):
    st.write(
        """
        - Quan sát dạng cắt hoặc giảm dần của các độ trễ.
        - Gợi ý giá trị ban đầu cho `p` và `q`.
        - Kiểm tra xem chuỗi sau xử lý đã có cấu trúc dễ mô hình hóa hơn chưa.

        Đây là công cụ hỗ trợ ra quyết định, không phải quy tắc cứng.
        """
    )

st.divider()

st.subheader("ARIMA(p,d,q)")
st.write(
    """
    ARIMA là mô hình kết hợp ba phần:
    - `p`: số bậc của thành phần AR
    - `d`: số lần sai phân
    - `q`: số bậc của thành phần MA

    Có thể hiểu ngắn gọn như sau:
    1. Trước hết, chuỗi được xử lý để trở nên ổn định hơn bằng sai phân (`d`).
    2. Sau đó, mô hình dùng giá trị quá khứ (`p`) và sai số quá khứ (`q`)
       để mô tả hành vi của chuỗi.
    3. Từ cấu trúc đó, mô hình đưa ra dự báo cho các bước tiếp theo.
    """
)

st.info(
    "ARIMA phù hợp với bài toán dự báo chuỗi thời gian có cấu trúc tương đối rõ, "
    "đặc biệt khi ta hiểu được xu hướng, tính dừng và mối liên hệ giữa các độ trễ."
)

with st.expander("Khi học ARIMA, nên nhớ điều gì"):
    st.write(
        """
        - Đừng chọn `p, d, q` chỉ theo cảm giác.
        - Hãy quan sát dữ liệu trước khi dựng mô hình.
        - Sai phân quá nhiều có thể làm mất thông tin hữu ích.
        - Mô hình tốt không chỉ là mô hình khớp dữ liệu cũ, mà còn phải dự báo hợp lý.
        """
    )

st.divider()
st.success("Trang này hiện tập trung vào phần giải thích khái niệm. Chưa đi sâu vào công thức hay triển khai mã.")
