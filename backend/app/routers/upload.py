"""
File upload router
"""
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict, Any, Optional
import os
import uuid
from datetime import datetime
from app.security import get_current_user, validate_file_type, validate_file_size
from app.database import get_supabase
from app.services.data_processor import data_processor
from app.services.pdf_parser import pdf_parser
from app.config import settings

router = APIRouter()

@router.post("/document")
async def upload_document(
    file: UploadFile = File(...),
    business_id: Optional[str] = None,
    current_user: Dict = Depends(get_current_user)
):
    """Upload and process financial document"""
    try:
        # Validate file
        if not validate_file_type(file.filename):
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file type. Allowed: {settings.ALLOWED_EXTENSIONS}"
            )
        
        # Read file content
        file_content = await file.read()
        file_size = len(file_content)
        
        if not validate_file_size(file_size):
            raise HTTPException(
                status_code=400,
                detail=f"File too large. Max size: {settings.MAX_UPLOAD_SIZE / 1024 / 1024}MB"
            )
        
        # Process file based on type
        file_ext = os.path.splitext(file.filename)[1].lower()
        
        if file_ext == '.csv':
            result = data_processor.parse_csv(file_content)
        elif file_ext in ['.xlsx', '.xls']:
            result = data_processor.parse_excel(file_content)
        elif file_ext == '.pdf':
            result = pdf_parser.parse_pdf(file_content)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type")
        
        if not result.get("success"):
            raise HTTPException(status_code=400, detail=result.get("error", "Processing failed"))
        
        # Store in database
        supabase = get_supabase()
        
        # Generate unique file path
        file_id = str(uuid.uuid4())
        file_path = f"{settings.UPLOAD_DIR}/{current_user['user_id']}/{file_id}{file_ext}"
        
        # Save to Supabase storage (optional)
        # storage_response = supabase.storage.from_('documents').upload(file_path, file_content)
        
        # Save metadata to database
        doc_data = {
            "id": file_id,
            "business_id": business_id or current_user["user_id"],
            "file_name": file.filename,
            "file_type": file_ext,
            "file_size": file_size,
            "file_path": file_path,
            "upload_status": "processed",
            "processed_at": datetime.utcnow().isoformat(),
            "extracted_data": result,
            "created_at": datetime.utcnow().isoformat()
        }
        
        db_response = supabase.table('uploaded_documents').insert(doc_data).execute()
        
        return {
            "success": True,
            "document_id": file_id,
            "file_name": file.filename,
            "processed_data": result,
            "message": "File uploaded and processed successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/documents")
async def get_uploaded_documents(
    business_id: Optional[str] = None,
    current_user: Dict = Depends(get_current_user)
):
    """Get all uploaded documents"""
    try:
        supabase = get_supabase()
        
        query = supabase.table('uploaded_documents').select('*')
        
        if business_id:
            query = query.eq('business_id', business_id)
        else:
            # Get all documents for user's businesses
            query = query.eq('business_id', current_user['user_id'])
        
        response = query.order('created_at', desc=True).execute()
        
        return {
            "success": True,
            "documents": response.data,
            "count": len(response.data)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/documents/{document_id}")
async def get_document(
    document_id: str,
    current_user: Dict = Depends(get_current_user)
):
    """Get specific document details"""
    try:
        supabase = get_supabase()
        
        response = supabase.table('uploaded_documents').select('*').eq('id', document_id).single().execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail="Document not found")
        
        return {
            "success": True,
            "document": response.data
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/documents/{document_id}")
async def delete_document(
    document_id: str,
    current_user: Dict = Depends(get_current_user)
):
    """Delete uploaded document"""
    try:
        supabase = get_supabase()
        
        response = supabase.table('uploaded_documents').delete().eq('id', document_id).execute()
        
        return {
            "success": True,
            "message": "Document deleted successfully"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
