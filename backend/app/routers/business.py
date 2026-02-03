"""
Business management router
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict, Any, Optional
from datetime import datetime
from app.security import get_current_user
from app.database import get_supabase

router = APIRouter()

class BusinessCreate(BaseModel):
    business_name: str
    industry: str
    registration_number: Optional[str] = None
    gst_number: Optional[str] = None
    pan_number: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    annual_revenue: Optional[float] = None
    employee_count: Optional[int] = None
    established_date: Optional[str] = None
    business_type: Optional[str] = None

@router.post("/")
async def create_business(
    business: BusinessCreate,
    current_user: Dict = Depends(get_current_user)
):
    """Create new business profile"""
    try:
        supabase = get_supabase()
        
        business_data = business.dict()
        business_data['user_id'] = current_user['user_id']
        business_data['created_at'] = datetime.utcnow().isoformat()
        business_data['updated_at'] = datetime.utcnow().isoformat()
        
        response = supabase.table('businesses').insert(business_data).execute()
        
        return {
            "success": True,
            "business": response.data[0] if response.data else business_data
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/")
async def get_businesses(current_user: Dict = Depends(get_current_user)):
    """Get all businesses for current user"""
    try:
        supabase = get_supabase()
        
        response = supabase.table('businesses')\
            .select('*')\
            .eq('user_id', current_user['user_id'])\
            .order('created_at', desc=True)\
            .execute()
        
        return {
            "success": True,
            "businesses": response.data,
            "count": len(response.data)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{business_id}")
async def get_business(
    business_id: str,
    current_user: Dict = Depends(get_current_user)
):
    """Get business by ID"""
    try:
        supabase = get_supabase()
        
        response = supabase.table('businesses')\
            .select('*')\
            .eq('id', business_id)\
            .single()\
            .execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail="Business not found")
        
        return {
            "success": True,
            "business": response.data
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{business_id}")
async def update_business(
    business_id: str,
    business: BusinessCreate,
    current_user: Dict = Depends(get_current_user)
):
    """Update business profile"""
    try:
        supabase = get_supabase()
        
        business_data = business.dict(exclude_unset=True)
        business_data['updated_at'] = datetime.utcnow().isoformat()
        
        response = supabase.table('businesses')\
            .update(business_data)\
            .eq('id', business_id)\
            .execute()
        
        return {
            "success": True,
            "business": response.data[0] if response.data else business_data
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
