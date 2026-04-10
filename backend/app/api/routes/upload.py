"""
SmartPredict AI — File Upload Routes
"""
import os
import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.config import settings
from app.services.data_cleaner import clean_dataset, get_column_info, get_data_summary

router = APIRouter(prefix="/api", tags=["upload"])

# In-memory store for datasets (replaces DB for simplicity)
datasets_store = {}


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Upload a CSV or Excel file for analysis."""
    
    # Validate file type
    allowed_extensions = [".csv", ".xlsx", ".xls"]
    ext = os.path.splitext(file.filename)[1].lower()
    
    if ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type '{ext}'. Please upload CSV or Excel files."
        )
    
    # Validate file size
    contents = await file.read()
    size_mb = len(contents) / (1024 * 1024)
    
    if size_mb > settings.MAX_UPLOAD_SIZE_MB:
        raise HTTPException(
            status_code=400,
            detail=f"File too large ({size_mb:.1f}MB). Maximum size is {settings.MAX_UPLOAD_SIZE_MB}MB."
        )
    
    # Save file
    file_id = str(uuid.uuid4())[:8]
    saved_filename = f"{file_id}{ext}"
    filepath = os.path.join(settings.UPLOAD_DIR, saved_filename)
    
    with open(filepath, "wb") as f:
        f.write(contents)
    
    try:
        # Clean and process
        df, cleaning_report = clean_dataset(filepath)
        columns_info = get_column_info(df)
        data_summary = get_data_summary(df)
        
        # Save cleaned version
        cleaned_path = os.path.join(settings.UPLOAD_DIR, f"{file_id}_cleaned.csv")
        df.to_csv(cleaned_path, index=False)
        
        # Store dataset info
        dataset_id = len(datasets_store) + 1
        datasets_store[dataset_id] = {
            "id": dataset_id,
            "file_id": file_id,
            "filename": saved_filename,
            "original_filename": file.filename,
            "filepath": filepath,
            "cleaned_filepath": cleaned_path,
            "row_count": len(df),
            "column_count": len(df.columns),
            "columns_info": columns_info,
            "file_size_bytes": len(contents),
            "status": "ready",
            "cleaning_report": cleaning_report,
            "data_summary": data_summary,
        }
        
        return {
            "dataset_id": dataset_id,
            "filename": file.filename,
            "row_count": len(df),
            "column_count": len(df.columns),
            "columns": list(df.columns),
            "status": "ready",
            "message": f"Successfully processed {file.filename}. {len(df):,} rows × {len(df.columns)} columns ready for analysis.",
            "cleaning_report": cleaning_report,
        }
        
    except Exception as e:
        # Clean up on error
        if os.path.exists(filepath):
            os.remove(filepath)
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")


@router.get("/datasets")
async def list_datasets():
    """List all uploaded datasets."""
    return {
        "datasets": [
            {
                "id": d["id"],
                "original_filename": d["original_filename"],
                "row_count": d["row_count"],
                "column_count": d["column_count"],
                "status": d["status"],
            }
            for d in datasets_store.values()
        ]
    }


@router.get("/datasets/{dataset_id}")
async def get_dataset(dataset_id: int):
    """Get dataset details."""
    if dataset_id not in datasets_store:
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    d = datasets_store[dataset_id]
    return {
        "id": d["id"],
        "original_filename": d["original_filename"],
        "row_count": d["row_count"],
        "column_count": d["column_count"],
        "columns_info": d["columns_info"],
        "status": d["status"],
        "cleaning_report": d["cleaning_report"],
        "data_summary": d["data_summary"],
    }


def get_dataset_store():
    """Expose datasets_store to other modules."""
    return datasets_store
