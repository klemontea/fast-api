import pandas as pd
from io import BytesIO
import tempfile
from fastapi import UploadFile


class DataModificationService:
    """Service for handling data modification via reference file mapping."""
    
    @staticmethod
    async def modify_data_via_reference(
        source_file: UploadFile,
        reference_file: UploadFile,
        key: str,
        target: str
    ):
        """
        Modify source file data using reference file mapping.
        
        Args:
            source_file: Excel file containing data to be modified
            reference_file: Excel file with mapping rules (KEY, AS-IS, TO-BE columns)
            key: Mapping key to filter the reference file
            target: Target column name in source file to apply mapping
            
        Returns:
            dict with either success (file path) or error information
        """
        try:
            # Read source file
            source_content = await source_file.read()
            source_df = pd.read_excel(BytesIO(source_content))
            
            # Read reference file
            reference_content = await reference_file.read()
            reference_df = pd.read_excel(BytesIO(reference_content))
            
            # Validate required columns in reference file
            required_cols = ['KEY', 'AS-IS', 'TO-BE']
            if not all(col in reference_df.columns for col in required_cols):
                return {
                    "error": f"Reference file must contain columns: {required_cols}",
                    "found_columns": list(reference_df.columns),
                    "success": False
                }
            
            # Validate target column exists in source file
            if target not in source_df.columns:
                return {
                    "error": f"Target column '{target}' not found in source file",
                    "available_columns": list(source_df.columns),
                    "success": False
                }
            
            # Filter reference data by key
            mapping_data = reference_df[reference_df['KEY'] == key]
            
            if mapping_data.empty:
                return {
                    "warning": f"No mapping found for key '{key}'",
                    "available_keys": reference_df['KEY'].unique().tolist(),
                    "success": False
                }
            
            # Create mapping dictionary from AS-IS to TO-BE
            mapping_dict = dict(zip(mapping_data['AS-IS'], mapping_data['TO-BE']))
            
            # Apply mapping to target column
            source_df[target] = source_df[target].replace(mapping_dict)
            
            # Create temporary file to save modified data
            with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp:
                tmp_path = tmp.name
                source_df.to_excel(tmp_path, index=False)
            
            return {
                "success": True,
                "file_path": tmp_path,
                "filename": f"modified_{source_file.filename}",
                "rows_modified": len(source_df),
                "mappings_applied": len(mapping_dict)
            }
        
        except Exception as e:
            return {
                "error": str(e),
                "message": "An error occurred while processing the files",
                "success": False
            }
