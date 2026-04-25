from __future__ import annotations

from pathlib import Path
from typing import BinaryIO

import pandas as pd


SAMPLE_DATASET_PATH = Path(__file__).resolve().parents[1] / "data" / "sample_series.csv"


def _validate_selected_columns(dataframe: pd.DataFrame, time_column: str, value_column: str) -> None:
    """Validate the selected time and value columns."""
    if time_column not in dataframe.columns:
        raise ValueError("Không tìm thấy cột thời gian trong dữ liệu.")

    if value_column not in dataframe.columns:
        raise ValueError("Không tìm thấy cột giá trị trong dữ liệu.")

    if time_column == value_column:
        raise ValueError("Cột thời gian và cột giá trị phải khác nhau.")


def load_csv_data(file_obj: BinaryIO) -> pd.DataFrame:
    """Load a full CSV file when the file size is reasonable."""
    try:
        file_obj.seek(0)
        dataframe = pd.read_csv(file_obj)
    except Exception as exc:  # pragma: no cover - defensive error mapping
        raise ValueError("Không thể đọc file CSV. Hãy kiểm tra định dạng file.") from exc

    if dataframe.empty:
        raise ValueError("File CSV không có dữ liệu.")

    return dataframe


def read_csv_columns(file_obj: BinaryIO) -> list[str]:
    """Read only CSV headers so large files do not load fully upfront."""
    try:
        file_obj.seek(0)
        columns = pd.read_csv(file_obj, nrows=0).columns.tolist()
    except Exception as exc:  # pragma: no cover - defensive error mapping
        raise ValueError("Không thể đọc header của file CSV.") from exc

    if not columns:
        raise ValueError("File CSV không có cột dữ liệu.")

    return columns


def load_csv_sample(
    file_obj: BinaryIO,
    time_column: str,
    value_column: str,
    sample_size: int,
) -> pd.DataFrame:
    """Load only selected columns and the first N rows from a CSV file."""
    if sample_size < 1:
        raise ValueError("Số sample phải lớn hơn 0.")

    try:
        file_obj.seek(0)
        dataframe = pd.read_csv(
            file_obj,
            usecols=[time_column, value_column],
            nrows=sample_size,
        )
    except ValueError as exc:
        raise ValueError("Không thể đọc các cột đã chọn từ file CSV.") from exc
    except Exception as exc:  # pragma: no cover - defensive error mapping
        raise ValueError("Không thể đọc sample từ file CSV.") from exc

    if dataframe.empty:
        raise ValueError("Không có dữ liệu trong sample đã chọn.")

    return dataframe


def load_sample_csv_data() -> pd.DataFrame:
    """Load the bundled sample dataset for demo purposes."""
    try:
        dataframe = pd.read_csv(SAMPLE_DATASET_PATH)
    except Exception as exc:  # pragma: no cover - file access depends on environment
        raise ValueError("Không thể đọc sample dataset trong thư mục data/.") from exc

    if dataframe.empty:
        raise ValueError("Sample dataset không có dữ liệu.")

    return dataframe


def prepare_time_series_dataframe(
    dataframe: pd.DataFrame,
    time_column: str,
    value_column: str,
) -> pd.DataFrame:
    """Convert the selected time column to datetime and sort the data."""
    _validate_selected_columns(dataframe, time_column, value_column)

    prepared_df = dataframe[[time_column, value_column]].copy()
    prepared_df[time_column] = pd.to_datetime(
        prepared_df[time_column].astype("string").str.strip(),
        errors="coerce",
        format="mixed",
    )

    invalid_time_rows = prepared_df[time_column].isna().sum()
    if invalid_time_rows == len(prepared_df):
        raise ValueError("Không thể chuyển cột thời gian sang `datetime`.")

    prepared_df = prepared_df.dropna(subset=[time_column]).sort_values(by=time_column)
    prepared_df = prepared_df.reset_index(drop=True)

    return prepared_df
