from __future__ import annotations

import pandas as pd


def create_time_series_figure(
    dataframe: pd.DataFrame,
    time_column: str,
    value_column: str,
    title: str,
) -> object:
    """Build a simple line chart for a time series."""
    try:
        import plotly.graph_objects as go
    except ModuleNotFoundError as exc:
        raise ValueError(
            "Thiếu package `plotly`. Hãy cài dependencies từ requirements.txt trước khi xem biểu đồ."
        ) from exc

    figure = go.Figure()
    figure.add_trace(
        go.Scatter(
            x=dataframe[time_column],
            y=dataframe[value_column],
            mode="lines+markers",
            name=value_column,
        )
    )
    figure.update_layout(
        title=title,
        xaxis_title=time_column,
        yaxis_title=value_column,
        margin=dict(l=20, r=20, t=50, b=20),
        height=380,
    )
    return figure


def apply_differencing(
    dataframe: pd.DataFrame,
    time_column: str,
    value_column: str,
    order: int,
) -> pd.DataFrame:
    """Return the original or differenced time series."""
    if order not in (0, 1, 2):
        raise ValueError("Chỉ hỗ trợ sai phân bậc 0, 1 hoặc 2.")

    result_df = dataframe[[time_column, value_column]].copy()
    result_df[value_column] = pd.to_numeric(result_df[value_column], errors="coerce")
    result_df = result_df.dropna(subset=[value_column]).reset_index(drop=True)

    if result_df.empty:
        raise ValueError("Cột giá trị không có dữ liệu số hợp lệ để vẽ biểu đồ hoặc sai phân.")

    if order > 0:
        result_df[value_column] = result_df[value_column].diff(periods=order)
        result_df = result_df.dropna(subset=[value_column]).reset_index(drop=True)

    if result_df.empty:
        raise ValueError("Không còn dữ liệu sau khi sai phân. Hãy kiểm tra số dòng của chuỗi.")

    return result_df
