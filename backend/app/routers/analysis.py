"""
Financial analysis router
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict, Any, Optional
from datetime import datetime
from app.security import get_current_user
from app.database import get_supabase
from app.services.financial_calculator import financial_calculator
from app.services.llm_service import llm_service

router = APIRouter()

class AnalysisRequest(BaseModel):
    business_id: str
    period_start: Optional[str] = None
    period_end: Optional[str] = None

@router.post("/financial-health")
async def analyze_financial_health(
    request: AnalysisRequest,
    current_user: Dict = Depends(get_current_user)
):
    """Analyze overall financial health"""
    try:
        supabase = get_supabase()
        
        # Get business info
        business = supabase.table('businesses').select('*').eq('id', request.business_id).single().execute()
        if not business.data:
            raise HTTPException(status_code=404, detail="Business not found")
        
        # Get financial data
        query = supabase.table('financial_data').select('*').eq('business_id', request.business_id)
        
        if request.period_start:
            query = query.gte('period_start', request.period_start)
        if request.period_end:
            query = query.lte('period_end', request.period_end)
        
        financial_records = query.order('period_end', desc=True).limit(12).execute()
        
        if not financial_records.data:
            raise HTTPException(status_code=404, detail="No financial data found")
        
        # Use most recent record
        latest_data = financial_records.data[0]
        
        # Add historical data for growth calculations
        if len(financial_records.data) > 1:
            latest_data['historical_data'] = financial_records.data
        
        # Calculate ratios
        ratios = financial_calculator.calculate_financial_ratios(latest_data)
        
        # Calculate scores
        health_score = financial_calculator.calculate_health_score(latest_data, ratios)
        credit_score = financial_calculator.calculate_credit_score(latest_data, ratios)
        
        # Assess risk
        risk_assessment = financial_calculator.assess_risk_level(latest_data, ratios)
        
        # Benchmark against industry
        industry_comparison = financial_calculator.benchmark_against_industry(
            ratios,
            business.data.get('industry', 'general')
        )
        
        # Get AI insights
        ai_analysis = await llm_service.analyze_financial_health(
            latest_data,
            business.data
        )
        
        # Prepare result
        analysis_result = {
            "health_score": health_score,
            "credit_score": credit_score,
            "risk_assessment": risk_assessment,
            "financial_ratios": ratios,
            "industry_comparison": industry_comparison,
            "ai_insights": ai_analysis.get('analysis', {}) if ai_analysis.get('success') else {},
            "period": {
                "start": latest_data.get('period_start'),
                "end": latest_data.get('period_end')
            }
        }
        
        # Save analysis to database
        analysis_record = {
            "business_id": request.business_id,
            "analysis_type": "comprehensive",
            "health_score": health_score,
            "credit_score": credit_score,
            "risk_level": risk_assessment['risk_level'],
            "insights": ai_analysis.get('analysis', {}),
            "recommendations": risk_assessment.get('recommendations', []),
            "financial_ratios": ratios,
            "benchmarks": industry_comparison,
            "created_at": datetime.utcnow().isoformat()
        }
        
        supabase.table('analysis_results').insert(analysis_record).execute()
        
        return {
            "success": True,
            "analysis": analysis_result
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history/{business_id}")
async def get_analysis_history(
    business_id: str,
    limit: int = 10,
    current_user: Dict = Depends(get_current_user)
):
    """Get analysis history"""
    try:
        supabase = get_supabase()
        
        response = supabase.table('analysis_results')\
            .select('*')\
            .eq('business_id', business_id)\
            .order('created_at', desc=True)\
            .limit(limit)\
            .execute()
        
        return {
            "success": True,
            "analyses": response.data,
            "count": len(response.data)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/ratios/{business_id}")
async def get_financial_ratios(
    business_id: str,
    current_user: Dict = Depends(get_current_user)
):
    """Get detailed financial ratios"""
    try:
        supabase = get_supabase()
        
        # Get latest financial data
        financial_record = supabase.table('financial_data')\
            .select('*')\
            .eq('business_id', business_id)\
            .order('period_end', desc=True)\
            .limit(1)\
            .single()\
            .execute()
        
        if not financial_record.data:
            raise HTTPException(status_code=404, detail="No financial data found")
        
        ratios = financial_calculator.calculate_financial_ratios(financial_record.data)
        
        return {
            "success": True,
            "ratios": ratios,
            "period": {
                "start": financial_record.data.get('period_start'),
                "end": financial_record.data.get('period_end')
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
