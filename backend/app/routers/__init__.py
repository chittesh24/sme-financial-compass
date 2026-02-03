"""
API Routers
"""
from .auth import router as auth_router
from .upload import router as upload_router
from .analysis import router as analysis_router
from .forecast import router as forecast_router
from .reports import router as reports_router
from .business import router as business_router
from .banking import router as banking_router
from .insights import router as insights_router

__all__ = [
    "auth_router",
    "upload_router",
    "analysis_router",
    "forecast_router",
    "reports_router",
    "business_router",
    "banking_router",
    "insights_router"
]
