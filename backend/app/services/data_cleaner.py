"""
SmartPredict AI — Data Cleaner Service

Auto-cleans and preprocesses uploaded CSV/Excel data.
"""
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Tuple


def clean_dataset(filepath: str) -> Tuple[pd.DataFrame, dict]:
    """
    Auto-clean a dataset file and return cleaned DataFrame + report.
    
    Steps:
    1. Read file (CSV or Excel)
    2. Normalize column names
    3. Remove duplicate rows
    4. Handle missing values
    5. Detect and convert data types
    6. Generate cleaning report
    """
    report = {
        "rows_removed": 0,
        "duplicates_removed": 0,
        "missing_values_filled": {},
        "columns_normalized": [],
        "type_conversions": {},
        "original_shape": [0, 0],
        "cleaned_shape": [0, 0],
    }
    
    # Step 1: Read file
    ext = Path(filepath).suffix.lower()
    if ext in [".xlsx", ".xls"]:
        df = pd.read_excel(filepath)
    elif ext == ".csv":
        df = pd.read_csv(filepath)
    else:
        raise ValueError(f"Unsupported file type: {ext}")
    
    report["original_shape"] = list(df.shape)
    
    # Step 2: Normalize column names
    original_cols = list(df.columns)
    df.columns = [
        str(col).strip()
            .lower()
            .replace(" ", "_")
            .replace("-", "_")
            .replace("(", "")
            .replace(")", "")
            .replace("/", "_")
            .replace(".", "_")
        for col in df.columns
    ]
    renamed = {orig: new for orig, new in zip(original_cols, df.columns) if orig != new}
    report["columns_normalized"] = list(renamed.keys())
    
    # Step 3: Remove completely empty rows
    empty_rows = df.isnull().all(axis=1).sum()
    df = df.dropna(how="all")
    report["rows_removed"] += int(empty_rows)
    
    # Step 4: Remove duplicates
    dup_count = df.duplicated().sum()
    df = df.drop_duplicates()
    report["duplicates_removed"] = int(dup_count)
    
    # Step 5: Handle missing values
    for col in df.columns:
        missing = df[col].isnull().sum()
        if missing == 0:
            continue
        
        if df[col].dtype in ["float64", "int64", "float32", "int32"]:
            # Numeric: fill with median
            median_val = df[col].median()
            df[col] = df[col].fillna(median_val)
            report["missing_values_filled"][col] = {
                "count": int(missing),
                "strategy": "median",
                "fill_value": float(median_val),
            }
        else:
            # Categorical: fill with mode
            mode_val = df[col].mode()
            if len(mode_val) > 0:
                df[col] = df[col].fillna(mode_val.iloc[0])
                report["missing_values_filled"][col] = {
                    "count": int(missing),
                    "strategy": "mode",
                    "fill_value": str(mode_val.iloc[0]),
                }
            else:
                df[col] = df[col].fillna("Unknown")
                report["missing_values_filled"][col] = {
                    "count": int(missing),
                    "strategy": "default",
                    "fill_value": "Unknown",
                }
    
    # Step 6: Detect dates and convert
    for col in df.columns:
        if df[col].dtype == "object":
            try:
                converted = pd.to_datetime(df[col], infer_datetime_format=True)
                if converted.notna().sum() > len(df) * 0.5:
                    df[col] = converted
                    report["type_conversions"][col] = "datetime"
            except (ValueError, TypeError):
                pass
        
        # Try numeric conversion for string columns
        if df[col].dtype == "object":
            try:
                converted = pd.to_numeric(df[col].str.replace(",", "").str.replace("$", "").str.replace("€", "").str.replace("£", "").str.strip(), errors="coerce")
                if converted.notna().sum() > len(df) * 0.7:
                    df[col] = converted
                    # Fill any NaN from conversion
                    df[col] = df[col].fillna(df[col].median())
                    report["type_conversions"][col] = "numeric"
            except (ValueError, TypeError, AttributeError):
                pass
    
    report["cleaned_shape"] = list(df.shape)
    report["rows_removed"] += report["original_shape"][0] - df.shape[0] - int(dup_count)
    
    return df, report


def get_column_info(df: pd.DataFrame) -> list[dict]:
    """Get metadata about each column."""
    columns_info = []
    for col in df.columns:
        info = {
            "name": col,
            "dtype": str(df[col].dtype),
            "non_null_count": int(df[col].notna().sum()),
            "unique_count": int(df[col].nunique()),
            "sample_values": [str(v) for v in df[col].dropna().head(5).tolist()],
        }
        
        # Add numeric stats if applicable
        if pd.api.types.is_numeric_dtype(df[col]):
            info["stats"] = {
                "min": float(df[col].min()) if not pd.isna(df[col].min()) else 0,
                "max": float(df[col].max()) if not pd.isna(df[col].max()) else 0,
                "mean": float(df[col].mean()) if not pd.isna(df[col].mean()) else 0,
                "median": float(df[col].median()) if not pd.isna(df[col].median()) else 0,
                "std": float(df[col].std()) if not pd.isna(df[col].std()) else 0,
            }
        
        columns_info.append(info)
    
    return columns_info


def get_data_summary(df: pd.DataFrame) -> dict:
    """Generate a high-level summary of the dataset."""
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
    datetime_cols = df.select_dtypes(include=["datetime64"]).columns.tolist()
    
    summary = {
        "total_rows": len(df),
        "total_columns": len(df.columns),
        "numeric_columns": numeric_cols,
        "categorical_columns": categorical_cols,
        "datetime_columns": datetime_cols,
        "memory_usage_mb": round(df.memory_usage(deep=True).sum() / 1048576, 2),
    }
    
    # Top-level numeric stats
    if numeric_cols:
        summary["numeric_summary"] = {}
        for col in numeric_cols:
            summary["numeric_summary"][col] = {
                "total": round(float(df[col].sum()), 2),
                "average": round(float(df[col].mean()), 2),
                "min": round(float(df[col].min()), 2),
                "max": round(float(df[col].max()), 2),
            }
    
    # Date range if applicable
    if datetime_cols:
        for col in datetime_cols:
            valid_dates = df[col].dropna()
            if len(valid_dates) > 0:
                summary["date_range"] = {
                    "column": col,
                    "start": str(valid_dates.min()),
                    "end": str(valid_dates.max()),
                }
                break
    
    return summary
