"""
Financial forecasting router
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict, Any, List
from datetime import datetime
from app.security import get_current_user
from app.database import get_supabase
from app.services.llm_service import llm_service

router = APIRouter()

class ForecastRequest(BaseModel):
    business_id: str
    forecast_period: str  # "3_months", "6_months", "1_year"
    forecast_type: str = "revenue"  # "revenue", "cashflow", "comprehensive"

@router.post("/generate")
async def generate_forecast(
    request: ForecastRequest,
    current_user: Dict = Depends(get_current_user)
):
    """Generate financial forecast"""
    try:
        supabase = get_supabase()
        
        # Get historical financial data
        financial_data = supabase.table('financial_data')\
            .select('*')\
            .eq('business_id', request.business_id)\
            .order('period_end', desc=True)\
            .limit(24)\
            .execute()
        
        if not financial_data.data or len(financial_data.data) < 3:
            raise HTTPException(
                status_code=400,
                detail="Insufficient historical data for forecasting (minimum 3 periods required)"
            )
        
        # Prepare historical data
        historical_records = [
            {
                "revenue": record.get('total_revenue', 0),
                "expenses": record.get('total_expenses', 0),
                "profit": record.get('net_profit', 0),
                "period": record.get('period_end')
            }
            for record in financial_data.data
        ]
        
        # Generate forecast using LLM
        forecast_result = await llm_service.generate_forecast(
            historical_data=historical_records,
            forecast_period=request.forecast_period
        )
        
        if not forecast_result.get('success'):
            raise HTTPException(status_code=500, detail="Forecast generation failed")
        
        # Save forecast to database
        forecast_record = {
            "business_id": request.business_id,
            "forecast_type": request.forecast_type,
            "forecast_period": request.forecast_period,
            "forecast_data": forecast_result.get('content'),
            "confidence_level": 75.0,  # Default confidence
            "methodology": "AI-powered analysis",
            "created_at": datetime.utcnow().isoformat()
        }
        
        supabase.table('forecasts').insert(forecast_record).execute()
        
        return {
            "success": True,
            "forecast": forecast_result.get('content'),
            "period": request.forecast_period,
            "historical_periods": len(historical_records)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history/{business_id}")
async def get_forecast_history(
    business_id: str,
    limit: int = 10,
    current_user: Dict = Depends(get_current_user)
):
    """Get forecast history"""
    try:
        supabase = get_supabase()
        
        response = supabase.table('forecasts')\
            .select('*')\
            .eq('business_id', business_id)\
            .order('created_at', desc=True)\
            .limit(limit)\
            .execute()
        
        return {
            "success": True,
            "forecasts": response.data,
            "count": len(response.data)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
