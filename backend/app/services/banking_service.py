"""
Banking API integration service (Plaid for international, Razorpay for India)
"""
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import httpx
from app.config import settings
from app.security import encrypt_sensitive_data, decrypt_sensitive_data

logger = logging.getLogger(__name__)

class BankingService:
    """Banking API integration service"""
    
    def __init__(self):
        # Plaid configuration
        self.plaid_client_id = settings.PLAID_CLIENT_ID
        self.plaid_secret = settings.PLAID_SECRET
        self.plaid_env = settings.PLAID_ENV
        self.plaid_base_url = self._get_plaid_url()
        
        # Razorpay configuration
        self.razorpay_key_id = settings.RAZORPAY_KEY_ID
        self.razorpay_key_secret = settings.RAZORPAY_KEY_SECRET
        self.razorpay_base_url = "https://api.razorpay.com/v1"
    
    def _get_plaid_url(self) -> str:
        """Get Plaid API URL based on environment"""
        urls = {
            "sandbox": "https://sandbox.plaid.com",
            "development": "https://development.plaid.com",
            "production": "https://production.plaid.com"
        }
        return urls.get(self.plaid_env, urls["sandbox"])
    
    # ============= PLAID INTEGRATION =============
    
    async def create_plaid_link_token(self, user_id: str, business_name: str) -> Dict[str, Any]:
        """Create Plaid Link token for connecting bank accounts"""
        try:
            if not self.plaid_client_id or not self.plaid_secret:
                return {
                    "success": False,
                    "error": "Plaid credentials not configured"
                }
            
            payload = {
                "client_id": self.plaid_client_id,
                "secret": self.plaid_secret,
                "user": {
                    "client_user_id": user_id,
                },
                "client_name": "SME Financial Compass",
                "products": ["transactions", "auth"],
                "country_codes": ["US", "CA", "GB", "IN"],
                "language": "en",
            }
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self.plaid_base_url}/link/token/create",
                    json=payload
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return {
                        "success": True,
                        "link_token": result.get("link_token"),
                        "expiration": result.get("expiration")
                    }
                else:
                    logger.error(f"Plaid link token error: {response.text}")
                    return {
                        "success": False,
                        "error": f"API error: {response.status_code}"
                    }
                    
        except Exception as e:
            logger.error(f"Plaid link token creation error: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def exchange_plaid_public_token(self, public_token: str) -> Dict[str, Any]:
        """Exchange public token for access token"""
        try:
            payload = {
                "client_id": self.plaid_client_id,
                "secret": self.plaid_secret,
                "public_token": public_token
            }
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self.plaid_base_url}/item/public_token/exchange",
                    json=payload
                )
                
                if response.status_code == 200:
                    result = response.json()
                    # Encrypt access token before storing
                    encrypted_token = encrypt_sensitive_data(result.get("access_token"))
                    return {
                        "success": True,
                        "access_token": encrypted_token,
                        "item_id": result.get("item_id")
                    }
                else:
                    logger.error(f"Plaid token exchange error: {response.text}")
                    return {
                        "success": False,
                        "error": f"API error: {response.status_code}"
                    }
                    
        except Exception as e:
            logger.error(f"Plaid token exchange error: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def get_plaid_accounts(self, encrypted_access_token: str) -> Dict[str, Any]:
        """Get bank account details from Plaid"""
        try:
            access_token = decrypt_sensitive_data(encrypted_access_token)
            
            payload = {
                "client_id": self.plaid_client_id,
                "secret": self.plaid_secret,
                "access_token": access_token
            }
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self.plaid_base_url}/accounts/get",
                    json=payload
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return {
                        "success": True,
                        "accounts": result.get("accounts", []),
                        "institution": result.get("item", {})
                    }
                else:
                    logger.error(f"Plaid accounts error: {response.text}")
                    return {
                        "success": False,
                        "error": f"API error: {response.status_code}"
                    }
                    
        except Exception as e:
            logger.error(f"Plaid accounts retrieval error: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def get_plaid_transactions(
        self,
        encrypted_access_token: str,
        start_date: str,
        end_date: str
    ) -> Dict[str, Any]:
        """Get transactions from Plaid"""
        try:
            access_token = decrypt_sensitive_data(encrypted_access_token)
            
            payload = {
                "client_id": self.plaid_client_id,
                "secret": self.plaid_secret,
                "access_token": access_token,
                "start_date": start_date,
                "end_date": end_date,
                "options": {
                    "count": 500,
                    "offset": 0
                }
            }
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self.plaid_base_url}/transactions/get",
                    json=payload
                )
                
                if response.status_code == 200:
                    result = response.json()
                    transactions = result.get("transactions", [])
                    
                    # Format transactions
                    formatted_txns = []
                    for txn in transactions:
                        formatted_txns.append({
                            "transaction_id": txn.get("transaction_id"),
                            "date": txn.get("date"),
                            "amount": txn.get("amount"),
                            "description": txn.get("name"),
                            "category": txn.get("category", ["Uncategorized"])[0] if txn.get("category") else "Uncategorized",
                            "merchant": txn.get("merchant_name"),
                            "account_id": txn.get("account_id")
                        })
                    
                    return {
                        "success": True,
                        "transactions": formatted_txns,
                        "total_count": result.get("total_transactions", len(formatted_txns))
                    }
                else:
                    logger.error(f"Plaid transactions error: {response.text}")
                    return {
                        "success": False,
                        "error": f"API error: {response.status_code}"
                    }
                    
        except Exception as e:
            logger.error(f"Plaid transactions retrieval error: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    # ============= RAZORPAY INTEGRATION =============
    
    async def get_razorpay_account_statement(
        self,
        account_id: str,
        from_date: str,
        to_date: str
    ) -> Dict[str, Any]:
        """Get account statement from Razorpay (for Indian businesses)"""
        try:
            if not self.razorpay_key_id or not self.razorpay_key_secret:
                return {
                    "success": False,
                    "error": "Razorpay credentials not configured"
                }
            
            params = {
                "from": from_date,
                "to": to_date,
                "count": 100
            }
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(
                    f"{self.razorpay_base_url}/transactions",
                    params=params,
                    auth=(self.razorpay_key_id, self.razorpay_key_secret)
                )
                
                if response.status_code == 200:
                    result = response.json()
                    transactions = result.get("items", [])
                    
                    # Format transactions
                    formatted_txns = []
                    for txn in transactions:
                        formatted_txns.append({
                            "transaction_id": txn.get("id"),
                            "date": datetime.fromtimestamp(txn.get("created_at", 0)).strftime("%Y-%m-%d"),
                            "amount": txn.get("amount", 0) / 100,  # Razorpay amounts are in paise
                            "currency": txn.get("currency", "INR"),
                            "description": txn.get("notes", {}).get("description", ""),
                            "type": txn.get("type"),
                            "status": txn.get("status")
                        })
                    
                    return {
                        "success": True,
                        "transactions": formatted_txns,
                        "count": len(formatted_txns)
                    }
                else:
                    logger.error(f"Razorpay API error: {response.text}")
                    return {
                        "success": False,
                        "error": f"API error: {response.status_code}"
                    }
                    
        except Exception as e:
            logger.error(f"Razorpay statement retrieval error: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def get_razorpay_balance(self) -> Dict[str, Any]:
        """Get Razorpay account balance"""
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(
                    f"{self.razorpay_base_url}/balance",
                    auth=(self.razorpay_key_id, self.razorpay_key_secret)
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return {
                        "success": True,
                        "balance": result.get("balance", 0) / 100,  # Convert from paise
                        "currency": result.get("currency", "INR")
                    }
                else:
                    logger.error(f"Razorpay balance error: {response.text}")
                    return {
                        "success": False,
                        "error": f"API error: {response.status_code}"
                    }
                    
        except Exception as e:
            logger.error(f"Razorpay balance retrieval error: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    # ============= HELPER METHODS =============
    
    def categorize_transaction(self, transaction: Dict[str, Any]) -> str:
        """Categorize transaction based on description"""
        description = transaction.get("description", "").lower()
        
        categories = {
            "salary": ["salary", "payroll", "wages"],
            "rent": ["rent", "lease"],
            "utilities": ["electricity", "water", "gas", "utility"],
            "inventory": ["inventory", "stock", "purchase", "supplier"],
            "marketing": ["marketing", "advertising", "promotion"],
            "travel": ["travel", "fuel", "transport"],
            "office": ["office", "stationery", "supplies"],
            "professional_fees": ["legal", "accounting", "consultant"],
            "insurance": ["insurance", "premium"],
            "loan_payment": ["loan", "emi", "interest"],
            "taxes": ["tax", "gst", "tds"],
        }
        
        for category, keywords in categories.items():
            if any(keyword in description for keyword in keywords):
                return category
        
        return "other"
    
    def analyze_cash_flow(self, transactions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze cash flow from transactions"""
        inflows = []
        outflows = []
        
        for txn in transactions:
            amount = abs(txn.get("amount", 0))
            if txn.get("amount", 0) > 0:
                inflows.append(amount)
            else:
                outflows.append(amount)
        
        return {
            "total_inflow": sum(inflows),
            "total_outflow": sum(outflows),
            "net_cashflow": sum(inflows) - sum(outflows),
            "inflow_count": len(inflows),
            "outflow_count": len(outflows),
            "average_inflow": sum(inflows) / len(inflows) if inflows else 0,
            "average_outflow": sum(outflows) / len(outflows) if outflows else 0
        }

# Singleton instance
banking_service = BankingService()
