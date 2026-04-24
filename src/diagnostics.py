from __future__ import annotations

import pandas as pd


def get_allowed_lag_range(series_length: int) -> tuple[int, int]:
    """Return a safe lag range for ACF/PACF exploration."""
    if series_length < 4:
        raise ValueError("Chuỗi quá ngắn để vẽ ACF/PACF. Cần ít nhất 4 điểm dữ liệu.")

    max_lag = min(20, series_length // 2)
    if max_lag < 1:
        raise ValueError("Chuỗi quá ngắn để chọn lag phù hợp.")

    return 1, max_lag


def create_acf_pacf_figures(
    dataframe: pd.DataFrame,
    value_column: str,
    lags: int,
) -> tuple[object, object]:
    """Create simple ACF and PACF bar charts."""
    try:
        import plotly.graph_objects as go
    except ModuleNotFoundError as exc:
        raise ValueError(
            "Thiếu package `plotly`. Hãy cài dependencies từ requirements.txt trước khi xem biểu đồ."
        ) from exc

    try:
        from statsmodels.tsa.stattools import acf, pacf
    except ModuleNotFoundError as exc:
        raise ValueError(
            "Thiếu package `statsmodels`. Hãy cài dependencies từ requirements.txt trước khi xem ACF/PACF."
        ) from exc

    series = pd.to_numeric(dataframe[value_column], errors="coerce").dropna()
    if len(series) < 4:
        raise ValueError("Chuỗi quá ngắn để vẽ ACF/PACF sau khi làm sạch dữ liệu.")

    _, max_lag = get_allowed_lag_range(len(series))
    safe_lags = min(lags, max_lag)

    acf_values = acf(series, nlags=safe_lags, fft=False)
    pacf_values = pacf(series, nlags=safe_lags, method="ywm")

    lag_index = list(range(len(acf_values)))
    acf_figure = go.Figure(
        data=[
            go.Bar(
                x=lag_index,
                y=acf_values,
                name="ACF",
            )
        ]
    )
    acf_figure.update_layout(
        title="ACF",
        xaxis_title="Lag",
        yaxis_title="Autocorrelation",
        margin=dict(l=20, r=20, t=50, b=20),
        height=320,
    )

    pacf_figure = go.Figure(
        data=[
            go.Bar(
                x=lag_index,
                y=pacf_values,
                name="PACF",
            )
        ]
    )
    pacf_figure.update_layout(
        title="PACF",
        xaxis_title="Lag",
        yaxis_title="Partial Autocorrelation",
        margin=dict(l=20, r=20, t=50, b=20),
        height=320,
    )

    return acf_figure, pacf_figure
