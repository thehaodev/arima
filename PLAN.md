# PLAN

## Mục tiêu hiện tại

Hoàn thiện một app Streamlit một trang để demo ARIMA theo flow trực quan, gọn và dễ dùng.

## Flow chính

1. Chọn dữ liệu:
   - dùng sample dataset trong `data/sample_series.csv`
   - hoặc upload CSV riêng
2. Quan sát chuỗi gốc
3. Thử differencing bậc 1 hoặc bậc 2
4. Xem ACF/PACF trên chuỗi đã được làm dừng
5. Chọn `p, d, q` và fit ARIMA
6. Xem forecast, residual và metrics ngay trong cùng trang

## Acceptance hiện tại

- app chạy bằng `streamlit run app.py`
- có thể dùng sample dataset hoặc upload CSV
- có biểu đồ chuỗi gốc
- có differencing bậc 1 và bậc 2
- có ACF/PACF và chọn số lag
- có fit `ARIMA(p,d,q)` thủ công
- có forecast trên tập test
- có forecast tương lai
- có `MAE` và `RMSE`
- có biểu đồ `Actual vs Forecast`
- có residual table/plot đơn giản để đọc nhanh

## Dọn dẹp project

- chỉ giữ một page chính là `page/3_ARIMA_Lab.py`
- không giữ page Overview/Theory/Results
- không giữ file utility thừa trong `data/`
- không giữ `__pycache__` trong repo
