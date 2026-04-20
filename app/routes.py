from fastapi import APIRouter, File, UploadFile, Form
from fastapi.responses import FileResponse
from app.services.data_modification import DataModificationService

router = APIRouter()


@router.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Welcome to the FastAPI Testing Application"}


@router.post("/modify-data")
async def modify_data_via_reference(
    source_file: UploadFile = File(...),
    reference_file: UploadFile = File(...),
    key: str = Form(...),
    target: str = Form(...)
):
    """
    Modify source file data using reference file mapping.
    
    Parameters:
    - source_file: Excel file containing data to be modified (must have headers in first row)
    - reference_file: Excel file with mapping rules containing columns: KEY, AS-IS, TO-BE
    - key: Mapping key to filter the reference file
    - target: Target column name in source file to apply mapping
    
    Returns:
    - Modified Excel file with applied mappings
    """
    result = await DataModificationService.modify_data_via_reference(
        source_file, reference_file, key, target
    )
    
    if result.get("success"):
        return FileResponse(
            path=result["file_path"],
            filename=result["filename"],
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        return result
