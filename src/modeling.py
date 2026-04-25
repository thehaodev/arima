from __future__ import annotations

from math import sqrt

import pandas as pd


def _prepare_numeric_model_dataframe(
    dataframe: pd.DataFrame,
    time_column: str,
    value_column: str,
) -> pd.DataFrame:
    """Keep the selected columns and coerce the value series to numeric."""
    model_df = dataframe[[time_column, value_column]].copy()
    model_df[value_column] = pd.to_numeric(model_df[value_column], errors="coerce")
    return model_df.dropna(subset=[value_column]).reset_index(drop=True)


def _calculate_error_metrics(test_forecast_df: pd.DataFrame) -> tuple[float, float]:
    """Calculate MAE and RMSE for the forecast dataframe."""
    mae = (test_forecast_df["actual"] - test_forecast_df["forecast"]).abs().mean()
    mse = ((test_forecast_df["actual"] - test_forecast_df["forecast"]) ** 2).mean()
    return float(mae), float(sqrt(mse))


def fit_arima_workflow(
    dataframe: pd.DataFrame,
    time_column: str,
    value_column: str,
    order: tuple[int, int, int],
    test_size: int,
    future_steps: int,
) -> dict:
    """Split data, fit ARIMA, refit on full data, and return forecast outputs."""
    try:
        from statsmodels.stats.diagnostic import acorr_ljungbox
        from statsmodels.tsa.arima.model import ARIMA
    except ModuleNotFoundError as exc:
        raise ValueError(
            "Thiếu package `statsmodels`. Hãy cài dependencies từ `requirements.txt` trước khi fit ARIMA."
        ) from exc

    p_value, d_value, q_value = order
    model_df = _prepare_numeric_model_dataframe(
        dataframe,
        time_column=time_column,
        value_column=value_column,
    )

    if len(model_df) < 8:
        raise ValueError("Chuỗi quá ngắn để fit ARIMA. Cần ít nhất 8 điểm dữ liệu số hợp lệ.")

    if test_size < 1 or test_size >= len(model_df):
        raise ValueError("Kích thước tập test không hợp lệ.")

    train_df = model_df.iloc[:-test_size].copy()
    test_df = model_df.iloc[-test_size:].copy()

    if len(train_df) <= max(p_value, d_value, q_value) + 1:
        raise ValueError("Tập train quá ngắn so với bộ tham số p, d, q đã chọn.")

    try:
        train_model = ARIMA(train_df[value_column], order=order).fit()
    except Exception as exc:  # pragma: no cover - depends on user input data
        raise ValueError(
            "ARIMA không fit được với dữ liệu hoặc bộ tham số hiện tại. Hãy thử giảm p, d, q hoặc tăng dữ liệu."
        ) from exc

    test_forecast_result = train_model.get_forecast(steps=len(test_df))
    test_forecast_values = test_forecast_result.predicted_mean
    test_conf_int = test_forecast_result.conf_int()
    test_forecast_df = pd.DataFrame(
        {
            time_column: test_df[time_column].tolist(),
            "actual": test_df[value_column].tolist(),
            "forecast": test_forecast_values.tolist(),
            "lower_ci": test_conf_int.iloc[:, 0].tolist(),
            "upper_ci": test_conf_int.iloc[:, 1].tolist(),
        }
    )
    test_forecast_df["residual"] = test_forecast_df["actual"] - test_forecast_df["forecast"]

    mae, rmse = _calculate_error_metrics(test_forecast_df)

    try:
        full_model = ARIMA(model_df[value_column], order=order).fit()
    except Exception as exc:  # pragma: no cover - depends on user input data
        raise ValueError("Không thể refit ARIMA trên toàn bộ dữ liệu sau khi đánh giá test.") from exc

    future_forecast_result = full_model.get_forecast(steps=future_steps)
    future_forecast_values = future_forecast_result.predicted_mean
    future_conf_int = future_forecast_result.conf_int()
    future_index = _build_future_index(model_df[time_column], future_steps)
    future_forecast_df = pd.DataFrame(
        {
            time_column: future_index,
            "forecast": future_forecast_values.tolist(),
            "lower_ci": future_conf_int.iloc[:, 0].tolist(),
            "upper_ci": future_conf_int.iloc[:, 1].tolist(),
        }
    )
    residual_df = pd.DataFrame(
        {
            time_column: model_df[time_column].tolist(),
            "residual": full_model.resid.tolist(),
        }
    )
    residual_summary = {
        "mean": float(residual_df["residual"].mean()),
        "std": float(residual_df["residual"].std(ddof=0)),
    }
    ljung_box_lag = max(1, min(10, len(residual_df) // 5))
    ljung_box_result = acorr_ljungbox(residual_df["residual"], lags=[ljung_box_lag], return_df=True)
    ljung_box_pvalue = float(ljung_box_result["lb_pvalue"].iloc[0])

    return {
        "order": order,
        "mae": float(mae),
        "rmse": float(rmse),
        "test_forecast_df": test_forecast_df,
        "future_forecast_df": future_forecast_df,
        "residual_df": residual_df,
        "residual_summary": residual_summary,
        "ljung_box_pvalue": ljung_box_pvalue,
    }


def _build_future_index(time_series: pd.Series, steps: int) -> list:
    """Build future timestamps using inferred frequency when possible."""
    if steps < 1:
        return []

    last_time = time_series.iloc[-1]
    inferred_freq = pd.infer_freq(time_series)

    if inferred_freq:
        return pd.date_range(start=last_time, periods=steps + 1, freq=inferred_freq)[1:].tolist()

    if len(time_series) >= 2:
        step = time_series.iloc[-1] - time_series.iloc[-2]
        if step != pd.Timedelta(0):
            return [last_time + step * (index + 1) for index in range(steps)]

    return [f"Bước {index + 1}" for index in range(steps)]
