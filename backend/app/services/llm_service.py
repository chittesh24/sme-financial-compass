"""
LLM Service using OpenRouter API
Supports GPT-4, Claude, and other models
"""
import asyncio
import logging
from typing import List, Dict, Any, Optional
import httpx
from app.config import settings

logger = logging.getLogger(__name__)

class LLMService:
    """Service for interacting with LLMs via OpenRouter"""
    
    def __init__(self):
        self.base_url = settings.OPENROUTER_BASE_URL
        self.api_key = settings.OPENROUTER_API_KEY
        self.default_model = settings.DEFAULT_MODEL
        self.fallback_model = settings.FALLBACK_MODEL
        
    async def generate_completion(
        self,
        prompt: str,
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2000,
        system_prompt: Optional[str] = None
    ) -> Dict[str, Any]:
        """Generate LLM completion"""
        try:
            model_to_use = model or self.default_model
            
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://sme-financial-compass.app",
                "X-Title": "SME Financial Compass"
            }
            
            payload = {
                "model": model_to_use,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens
            }
            
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=payload
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return {
                        "success": True,
                        "content": result["choices"][0]["message"]["content"],
                        "model": result.get("model", model_to_use),
                        "usage": result.get("usage", {})
                    }
                else:
                    logger.error(f"OpenRouter API error: {response.status_code} - {response.text}")
                    # Try fallback model
                    if model_to_use != self.fallback_model:
                        return await self.generate_completion(
                            prompt, self.fallback_model, temperature, max_tokens, system_prompt
                        )
                    return {
                        "success": False,
                        "error": f"API error: {response.status_code}"
                    }
                    
        except Exception as e:
            logger.error(f"LLM generation error: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def analyze_financial_health(self, financial_data: Dict[str, Any], business_info: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze financial health using LLM"""
        system_prompt = """You are an expert financial analyst specializing in SME financial health assessment.
        Analyze the provided financial data and provide actionable insights, risk assessment, and recommendations.
        Focus on: creditworthiness, liquidity, profitability, efficiency, and growth potential."""
        
        prompt = f"""
        Analyze the financial health of this business:
        
        Business Information:
        - Name: {business_info.get('business_name', 'N/A')}
        - Industry: {business_info.get('industry', 'N/A')}
        - Established: {business_info.get('established_date', 'N/A')}
        
        Financial Data:
        - Total Revenue: ₹{financial_data.get('total_revenue', 0):,.2f}
        - Total Expenses: ₹{financial_data.get('total_expenses', 0):,.2f}
        - Net Profit: ₹{financial_data.get('net_profit', 0):,.2f}
        - Profit Margin: {financial_data.get('profit_margin', 0):.2f}%
        - Current Ratio: {financial_data.get('current_ratio', 0):.2f}
        - Debt-to-Equity: {financial_data.get('debt_to_equity', 0):.2f}
        - Cash Balance: ₹{financial_data.get('cash_balance', 0):,.2f}
        
        Provide:
        1. Overall health score (0-100)
        2. Key strengths (3-5 points)
        3. Key concerns (3-5 points)
        4. Specific recommendations (5-7 actionable items)
        5. Risk assessment (low/medium/high with explanation)
        6. Credit score estimate (300-900)
        
        Format as JSON with keys: health_score, strengths, concerns, recommendations, risk_level, credit_score, summary
        """
        
        result = await self.generate_completion(
            prompt=prompt,
            system_prompt=system_prompt,
            temperature=0.5,
            max_tokens=2500
        )
        
        if result["success"]:
            try:
                import json
                # Try to parse JSON from response
                content = result["content"]
                # Extract JSON if wrapped in markdown
                if "```json" in content:
                    content = content.split("```json")[1].split("```")[0].strip()
                elif "```" in content:
                    content = content.split("```")[1].split("```")[0].strip()
                
                parsed_result = json.loads(content)
                return {
                    "success": True,
                    "analysis": parsed_result
                }
            except json.JSONDecodeError:
                # If JSON parsing fails, return raw content
                return {
                    "success": True,
                    "analysis": {
                        "summary": result["content"],
                        "health_score": 0,
                        "credit_score": 0
                    }
                }
        else:
            return result
    
    async def generate_forecast(self, historical_data: List[Dict[str, Any]], forecast_period: str) -> Dict[str, Any]:
        """Generate financial forecast using LLM"""
        system_prompt = """You are a financial forecasting expert. Analyze historical trends and generate realistic forecasts."""
        
        # Prepare historical data summary
        data_summary = "\n".join([
            f"Period {i+1}: Revenue ₹{d.get('revenue', 0):,.2f}, Expenses ₹{d.get('expenses', 0):,.2f}"
            for i, d in enumerate(historical_data[-12:])  # Last 12 periods
        ])
        
        prompt = f"""
        Based on this historical financial data:
        
        {data_summary}
        
        Generate a {forecast_period} forecast with:
        1. Projected revenue (with confidence intervals)
        2. Projected expenses
        3. Expected profit/loss
        4. Key assumptions
        5. Risk factors
        6. Growth rate estimates
        
        Provide realistic, data-driven forecasts. Format as JSON.
        """
        
        result = await self.generate_completion(
            prompt=prompt,
            system_prompt=system_prompt,
            temperature=0.3,
            max_tokens=2000
        )
        
        return result
    
    async def generate_recommendations(self, business_context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate business recommendations"""
        system_prompt = """You are a business advisor specializing in SMEs. Provide practical, actionable recommendations."""
        
        prompt = f"""
        For this business:
        Industry: {business_context.get('industry', 'N/A')}
        Current Situation: {business_context.get('situation', 'N/A')}
        Goals: {business_context.get('goals', 'N/A')}
        
        Provide:
        1. Cost optimization strategies (5 specific actions)
        2. Revenue growth opportunities (5 ideas)
        3. Working capital improvement tactics (3-5 points)
        4. Suitable financial products (loans, credit lines, etc.)
        5. Tax optimization tips (legal strategies)
        
        Format as JSON with actionable items.
        """
        
        result = await self.generate_completion(
            prompt=prompt,
            system_prompt=system_prompt,
            temperature=0.6,
            max_tokens=2500
        )
        
        return result
    
    async def translate_content(self, content: str, target_language: str) -> Dict[str, Any]:
        """Translate content to target language"""
        language_map = {
            "hi": "Hindi",
            "te": "Telugu",
            "ta": "Tamil",
            "kn": "Kannada",
            "mr": "Marathi",
            "gu": "Gujarati",
            "bn": "Bengali"
        }
        
        target_lang_name = language_map.get(target_language, target_language)
        
        prompt = f"""
        Translate the following financial/business content to {target_lang_name}.
        Maintain professional terminology and accuracy.
        
        Content to translate:
        {content}
        
        Provide only the translated text, no explanations.
        """
        
        result = await self.generate_completion(
            prompt=prompt,
            temperature=0.3,
            max_tokens=3000
        )
        
        return result
    
    async def chat_response(self, user_message: str, conversation_history: List[Dict[str, str]], business_context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate conversational response for insights chat"""
        system_prompt = f"""You are a friendly financial advisor assistant for SME Financial Compass.
        Help business owners understand their financials and make better decisions.
        
        Business Context:
        - Industry: {business_context.get('industry', 'General')}
        - Revenue: ₹{business_context.get('revenue', 0):,.0f}
        - Health Score: {business_context.get('health_score', 'N/A')}
        
        Be concise, helpful, and action-oriented. Use simple language."""
        
        # Build message history
        messages = []
        for msg in conversation_history[-5:]:  # Last 5 messages
            messages.append(msg)
        messages.append({"role": "user", "content": user_message})
        
        # Convert to prompt
        conversation = "\n".join([f"{m['role']}: {m['content']}" for m in messages])
        
        result = await self.generate_completion(
            prompt=conversation,
            system_prompt=system_prompt,
            temperature=0.7,
            max_tokens=500
        )
        
        return result

# Singleton instance
llm_service = LLMService()
