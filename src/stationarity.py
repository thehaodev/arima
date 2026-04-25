from __future__ import annotations

import pandas as pd

from src.plotting import create_line_figure


def create_time_series_figure(
    dataframe: pd.DataFrame,
    time_column: str,
    value_column: str,
    title: str,
) -> object:
    """Build a line chart for a time series."""
    return create_line_figure(
        x_values=dataframe[time_column],
        y_values=dataframe[value_column],
        name=value_column,
        title=title,
        xaxis_title=time_column,
        yaxis_title=value_column,
    )


def apply_differencing(
    dataframe: pd.DataFrame,
    time_column: str,
    value_column: str,
    order: int,
) -> pd.DataFrame:
    """Return the original series or the correctly differenced series."""
    if order not in (0, 1, 2):
        raise ValueError("Chỉ hỗ trợ sai phân bậc 0, 1 hoặc 2.")

    result_df = dataframe[[time_column, value_column]].copy()
    result_df[value_column] = pd.to_numeric(result_df[value_column], errors="coerce")
    result_df = result_df.dropna(subset=[value_column]).reset_index(drop=True)

    if result_df.empty:
        raise ValueError("Cột giá trị không có dữ liệu số hợp lệ để vẽ biểu đồ hoặc sai phân.")

    for _ in range(order):
        result_df[value_column] = result_df[value_column].diff()
        result_df = result_df.dropna(subset=[value_column]).reset_index(drop=True)

    if result_df.empty:
        raise ValueError("Không còn dữ liệu sau khi sai phân. Hãy kiểm tra số dòng của chuỗi.")

    return result_df


def run_adf_test(dataframe: pd.DataFrame, value_column: str) -> dict:
    """Run ADF on a numeric series and return statistic plus p-value."""
    try:
        from statsmodels.tsa.stattools import adfuller
    except ModuleNotFoundError as exc:
        raise ValueError(
            "Thiếu package `statsmodels`. Hãy cài dependencies từ `requirements.txt` trước khi chạy ADF."
        ) from exc

    series = _extract_numeric_series(dataframe, value_column)
    if len(series) < 4:
        raise ValueError("Chuỗi quá ngắn để chạy ADF.")

    statistic, p_value, *_ = adfuller(series, autolag="AIC")
    return {
        "statistic": float(statistic),
        "p_value": float(p_value),
        "decision": _describe_adf_p_value(float(p_value)),
    }


def suggest_d_order(
    dataframe: pd.DataFrame,
    time_column: str,
    value_column: str,
    alpha: float = 0.05,
) -> tuple[int, pd.DataFrame]:
    """Suggest a small differencing order using ADF and KPSS when possible."""
    trace_rows = []
    suggested_d = 2

    for order in (0, 1, 2):
        try:
            differenced_df = apply_differencing(
                dataframe,
                time_column=time_column,
                value_column=value_column,
                order=order,
            )
            adf_result = run_adf_test(differenced_df, value_column)
            kpss_result = _run_kpss_test(differenced_df, value_column)
            is_stationary = adf_result["p_value"] < alpha and (
                kpss_result["p_value"] is None or kpss_result["p_value"] > alpha
            )
            decision = "Gợi ý dừng" if is_stationary else "Chưa đủ tín hiệu dừng"
        except ValueError as error:
            adf_result = {"statistic": None, "p_value": None}
            kpss_result = {"statistic": None, "p_value": None}
            decision = f"Không đánh giá được: {error}"
            is_stationary = False

        trace_rows.append(
            {
                "d": order,
                "adf_stat": adf_result["statistic"],
                "adf_pvalue": adf_result["p_value"],
                "kpss_stat": kpss_result["statistic"],
                "kpss_pvalue": kpss_result["p_value"],
                "decision": decision,
            }
        )

        if is_stationary:
            suggested_d = order
            break

    return suggested_d, pd.DataFrame(trace_rows)


def _extract_numeric_series(dataframe: pd.DataFrame, value_column: str) -> pd.Series:
    """Extract a clean numeric series from the selected dataframe column."""
    series = pd.to_numeric(dataframe[value_column], errors="coerce").dropna()
    if series.empty:
        raise ValueError("Không có đủ dữ liệu số hợp lệ để phân tích tính dừng.")
    return series


def _run_kpss_test(dataframe: pd.DataFrame, value_column: str) -> dict:
    """Run KPSS on a numeric series and return statistic plus p-value."""
    try:
        from statsmodels.tsa.stattools import kpss
    except ModuleNotFoundError as exc:
        raise ValueError(
            "Thiếu package `statsmodels`. Hãy cài dependencies từ `requirements.txt` trước khi chạy KPSS."
        ) from exc

    series = _extract_numeric_series(dataframe, value_column)
    if len(series) < 4:
        raise ValueError("Chuỗi quá ngắn để chạy KPSS.")

    try:
        statistic, p_value, *_ = kpss(series, regression="c", nlags="auto")
    except Exception:
        return {"statistic": None, "p_value": None}

    return {
        "statistic": float(statistic),
        "p_value": float(p_value),
    }


def _describe_adf_p_value(p_value: float) -> str:
    """Return a short interpretation for the ADF p-value."""
    if p_value < 0.05:
        return "p-value nhỏ: có bằng chứng mạnh hơn để xem chuỗi là dừng."
    return "p-value lớn: chưa có đủ bằng chứng để xem chuỗi là dừng."
