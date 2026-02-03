"""
AI Insights router (Chat interface)
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from app.security import get_current_user
from app.database import get_supabase
from app.services.llm_service import llm_service

router = APIRouter()

class ChatMessage(BaseModel):
    message: str
    business_id: Optional[str] = None

class ChatHistory(BaseModel):
    messages: List[Dict[str, str]]

@router.post("/chat")
async def chat_with_ai(
    request: ChatMessage,
    current_user: Dict = Depends(get_current_user)
):
    """Chat with AI financial advisor"""
    try:
        # Get business context if provided
        business_context = {}
        if request.business_id:
            supabase = get_supabase()
            
            # Get business info
            business = supabase.table('businesses').select('*').eq('id', request.business_id).single().execute()
            if business.data:
                business_context = business.data
            
            # Get latest analysis
            analysis = supabase.table('analysis_results')\
                .select('*')\
                .eq('business_id', request.business_id)\
                .order('created_at', desc=True)\
                .limit(1)\
                .execute()
            
            if analysis.data:
                business_context.update({
                    'health_score': analysis.data[0].get('health_score'),
                    'credit_score': analysis.data[0].get('credit_score'),
                    'risk_level': analysis.data[0].get('risk_level')
                })
        
        # Generate AI response
        response = await llm_service.chat_response(
            user_message=request.message,
            conversation_history=[],
            business_context=business_context
        )
        
        if response.get('success'):
            return {
                "success": True,
                "message": response.get('content'),
                "model": response.get('model')
            }
        else:
            raise HTTPException(status_code=500, detail=response.get('error'))
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/recommendations")
async def get_recommendations(
    business_id: str,
    current_user: Dict = Depends(get_current_user)
):
    """Get AI-generated business recommendations"""
    try:
        supabase = get_supabase()
        
        # Get business info and latest analysis
        business = supabase.table('businesses').select('*').eq('id', business_id).single().execute()
        analysis = supabase.table('analysis_results')\
            .select('*')\
            .eq('business_id', business_id)\
            .order('created_at', desc=True)\
            .limit(1)\
            .execute()
        
        if not business.data:
            raise HTTPException(status_code=404, detail="Business not found")
        
        # Prepare business context
        business_context = {
            "industry": business.data.get('industry'),
            "situation": f"Health Score: {analysis.data[0].get('health_score', 'N/A')}, Risk: {analysis.data[0].get('risk_level', 'Unknown')}" if analysis.data else "No analysis available",
            "goals": "Improve financial health and profitability"
        }
        
        # Get AI recommendations
        recommendations = await llm_service.generate_recommendations(business_context)
        
        if recommendations.get('success'):
            return {
                "success": True,
                "recommendations": recommendations.get('content')
            }
        else:
            raise HTTPException(status_code=500, detail=recommendations.get('error'))
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
