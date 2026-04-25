# ARIMA Demo Lab

Ứng dụng Streamlit này tập trung vào một trải nghiệm demo trực quan duy nhất:
chọn dữ liệu, quan sát chuỗi, thử differencing, xem ACF/PACF,
fit ARIMA và đọc forecast ngay trong cùng một trang.

## Cách chạy

### Git Bash

```bash
python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
streamlit run app.py
```

### PowerShell

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

## Flow demo

Ứng dụng hiện đi theo đúng flow này:

1. Chọn dữ liệu:
   - dùng sample dataset có sẵn trong `data/sample_series.csv`
   - hoặc upload CSV riêng
2. Quan sát chuỗi gốc
3. Thử differencing bậc 1 hoặc bậc 2
4. Xem ACF/PACF để gợi ý `q` và `p` ban đầu
5. Gợi ý `d` bằng stationarity checks rồi vẫn cho phép chỉnh tay
6. Chọn `p, d, q` và fit ARIMA
7. Xem `Actual vs Forecast`, residual diagnostics, forecast tương lai, `MAE` và `RMSE` ngay cuối trang

## Yêu cầu dữ liệu đầu vào

CSV nên có ít nhất:

- một cột thời gian có thể convert sang `datetime`
- một cột giá trị có thể convert sang số

App sẽ tự:

- convert cột thời gian sang `datetime`
- sort tăng dần theo thời gian
- làm sạch dữ liệu không hợp lệ ở các bước cần thiết

## Cấu trúc project

```text
.
├── app.py
├── page/
│   └── 3_ARIMA_Lab.py
├── src/
│   ├── app_state.py
│   ├── data_utils.py
│   ├── diagnostics.py
│   ├── modeling.py
│   ├── plotting.py
│   └── stationarity.py
├── data/
│   └── sample_series.csv
├── requirements.txt
└── PLAN.md
```

## Ghi chú

- App không dùng `auto_arima`.
- Kết quả forecast được giữ trong `st.session_state` để vẫn hiển thị ổn định sau khi bấm nút chạy mô hình.
- Logic ARIMA cốt lõi được giữ trong `src/modeling.py`.
- Sample dataset hiện đủ dài để demo đầy đủ flow ARIMA.
- Future forecast được tạo sau khi refit mô hình trên toàn bộ dữ liệu.
