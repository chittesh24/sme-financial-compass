"""
Banking integration router
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict, Any
from datetime import datetime, timedelta
from app.security import get_current_user
from app.database import get_supabase
from app.services.banking_service import banking_service

router = APIRouter()

class PlaidLinkRequest(BaseModel):
    business_id: str

class PlaidTokenExchange(BaseModel):
    public_token: str
    business_id: str

@router.post("/plaid/link-token")
async def create_plaid_link_token(
    request: PlaidLinkRequest,
    current_user: Dict = Depends(get_current_user)
):
    """Create Plaid Link token"""
    result = await banking_service.create_plaid_link_token(
        user_id=current_user['user_id'],
        business_name=f"Business {request.business_id}"
    )
    
    if result.get('success'):
        return result
    else:
        raise HTTPException(status_code=500, detail=result.get('error'))

@router.post("/plaid/exchange-token")
async def exchange_plaid_token(
    request: PlaidTokenExchange,
    current_user: Dict = Depends(get_current_user)
):
    """Exchange Plaid public token for access token"""
    result = await banking_service.exchange_plaid_public_token(request.public_token)
    
    if result.get('success'):
        # Save connection to database
        supabase = get_supabase()
        connection_data = {
            "business_id": request.business_id,
            "provider": "plaid",
            "access_token_encrypted": result['access_token'],
            "connection_status": "active",
            "created_at": datetime.utcnow().isoformat()
        }
        supabase.table('banking_connections').insert(connection_data).execute()
        return {"success": True, "message": "Bank connected successfully"}
    else:
        raise HTTPException(status_code=500, detail=result.get('error'))

@router.get("/transactions/{business_id}")
async def get_transactions(
    business_id: str,
    days: int = 30,
    current_user: Dict = Depends(get_current_user)
):
    """Get banking transactions"""
    try:
        supabase = get_supabase()
        
        # Get banking connection
        connection = supabase.table('banking_connections')\
            .select('*')\
            .eq('business_id', business_id)\
            .eq('connection_status', 'active')\
            .limit(1)\
            .execute()
        
        if not connection.data:
            return {"success": True, "transactions": [], "message": "No banking connection found"}
        
        # Get transactions from Plaid
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        
        result = await banking_service.get_plaid_transactions(
            encrypted_access_token=connection.data[0]['access_token_encrypted'],
            start_date=start_date,
            end_date=end_date
        )
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
