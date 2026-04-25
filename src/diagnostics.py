from __future__ import annotations

import pandas as pd

from src.plotting import create_bar_figure


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
    """Create ACF and PACF bar charts."""
    try:
        from statsmodels.tsa.stattools import acf, pacf
    except ModuleNotFoundError as exc:
        raise ValueError(
            "Thiếu package `statsmodels`. Hãy cài dependencies từ `requirements.txt` trước khi xem ACF/PACF."
        ) from exc

    series = pd.to_numeric(dataframe[value_column], errors="coerce").dropna()
    if len(series) < 4:
        raise ValueError("Chuỗi quá ngắn để vẽ ACF/PACF sau khi làm sạch dữ liệu.")

    _, max_lag = get_allowed_lag_range(len(series))
    safe_lags = min(lags, max_lag)

    acf_values = acf(series, nlags=safe_lags, fft=False)
    pacf_values = pacf(series, nlags=safe_lags, method="ywm")
    lag_index = list(range(len(acf_values)))
    acf_figure = create_bar_figure(
        x_values=lag_index,
        y_values=acf_values,
        name="ACF",
        title="ACF",
        xaxis_title="Lag",
        yaxis_title="Autocorrelation",
    )
    pacf_figure = create_bar_figure(
        x_values=lag_index,
        y_values=pacf_values,
        name="PACF",
        title="PACF",
        xaxis_title="Lag",
        yaxis_title="Partial Autocorrelation",
    )

    return acf_figure, pacf_figure


def create_acf_figure(
    dataframe: pd.DataFrame,
    value_column: str,
    lags: int,
    title: str = "ACF",
) -> object:
    """Create a single ACF chart for a numeric series."""
    try:
        from statsmodels.tsa.stattools import acf
    except ModuleNotFoundError as exc:
        raise ValueError(
            "Thiếu package `statsmodels`. Hãy cài dependencies từ `requirements.txt` trước khi xem ACF."
        ) from exc

    series = pd.to_numeric(dataframe[value_column], errors="coerce").dropna()
    if len(series) < 4:
        raise ValueError("Chuỗi quá ngắn để vẽ ACF.")

    _, max_lag = get_allowed_lag_range(len(series))
    safe_lags = min(lags, max_lag)
    acf_values = acf(series, nlags=safe_lags, fft=False)
    lag_index = list(range(len(acf_values)))

    return create_bar_figure(
        x_values=lag_index,
        y_values=acf_values,
        name=title,
        title=title,
        xaxis_title="Lag",
        yaxis_title="Autocorrelation",
    )
