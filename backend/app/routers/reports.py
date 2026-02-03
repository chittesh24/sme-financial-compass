"""
Reports generation router
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict, Any, Optional
from datetime import datetime
from app.security import get_current_user
from app.database import get_supabase
from app.services.translation_service import translation_service

router = APIRouter()

class ReportRequest(BaseModel):
    business_id: str
    report_type: str  # "financial_health", "investor", "tax", "comprehensive"
    language: str = "en"
    include_charts: bool = True

@router.post("/generate")
async def generate_report(
    request: ReportRequest,
    current_user: Dict = Depends(get_current_user)
):
    """Generate financial report"""
    try:
        supabase = get_supabase()
        
        # Get business and analysis data
        business = supabase.table('businesses').select('*').eq('id', request.business_id).single().execute()
        analysis = supabase.table('analysis_results')\
            .select('*')\
            .eq('business_id', request.business_id)\
            .order('created_at', desc=True)\
            .limit(1)\
            .execute()
        
        if not business.data:
            raise HTTPException(status_code=404, detail="Business not found")
        
        # Prepare report data
        report_data = {
            "business_name": business.data.get('business_name'),
            "industry": business.data.get('industry'),
            "generated_date": datetime.utcnow().isoformat(),
            "report_type": request.report_type,
            "analysis": analysis.data[0] if analysis.data else {},
            "language": request.language
        }
        
        # Translate if needed
        if request.language != "en":
            translated = await translation_service.translate_report(report_data, request.language)
            if translated.get('success'):
                report_data = translated['translated_report']
        
        # Save report
        report_record = {
            "business_id": request.business_id,
            "report_type": request.report_type,
            "report_name": f"{request.report_type.replace('_', ' ').title()} Report",
            "report_data": report_data,
            "language": request.language,
            "created_at": datetime.utcnow().isoformat()
        }
        
        db_response = supabase.table('reports').insert(report_record).execute()
        
        return {
            "success": True,
            "report": report_data,
            "report_id": db_response.data[0]['id'] if db_response.data else None
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{business_id}")
async def get_reports(
    business_id: str,
    current_user: Dict = Depends(get_current_user)
):
    """Get all reports for business"""
    try:
        supabase = get_supabase()
        
        response = supabase.table('reports')\
            .select('*')\
            .eq('business_id', business_id)\
            .order('created_at', desc=True)\
            .execute()
        
        return {
            "success": True,
            "reports": response.data,
            "count": len(response.data)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
