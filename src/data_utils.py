from __future__ import annotations

from typing import BinaryIO

import pandas as pd


def load_csv_data(file_obj: BinaryIO) -> pd.DataFrame:
    """Load a CSV file uploaded from Streamlit."""
    try:
        dataframe = pd.read_csv(file_obj)
    except Exception as exc:  # pragma: no cover - defensive error mapping
        raise ValueError("Không thể đọc file CSV. Hãy kiểm tra định dạng file.") from exc

    if dataframe.empty:
        raise ValueError("File CSV không có dữ liệu.")

    return dataframe


def prepare_time_series_dataframe(
    dataframe: pd.DataFrame,
    time_column: str,
    value_column: str,
) -> pd.DataFrame:
    """Convert the selected time column to datetime and sort the data."""
    if time_column not in dataframe.columns:
        raise ValueError("Không tìm thấy cột thời gian trong dữ liệu.")

    if value_column not in dataframe.columns:
        raise ValueError("Không tìm thấy cột giá trị trong dữ liệu.")

    if time_column == value_column:
        raise ValueError("Cột thời gian và cột giá trị phải khác nhau.")

    prepared_df = dataframe[[time_column, value_column]].copy()
    prepared_df[time_column] = pd.to_datetime(
        prepared_df[time_column].astype("string").str.strip(),
        errors="coerce",
        format="mixed",
    )

    invalid_time_rows = prepared_df[time_column].isna().sum()
    if invalid_time_rows == len(prepared_df):
        raise ValueError("Không thể convert cột thời gian sang datetime.")

    prepared_df = prepared_df.dropna(subset=[time_column]).sort_values(by=time_column)
    prepared_df = prepared_df.reset_index(drop=True)

    return prepared_df
