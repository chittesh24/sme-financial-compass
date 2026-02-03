"""
Financial calculation engine for ratios, metrics, and analysis
"""
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import statistics

logger = logging.getLogger(__name__)

class FinancialCalculator:
    """Calculate financial ratios, scores, and metrics"""
    
    def __init__(self):
        self.industry_benchmarks = self._load_industry_benchmarks()
    
    def calculate_financial_ratios(self, financial_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate all financial ratios"""
        ratios = {}
        
        # Profitability Ratios
        ratios["profitability"] = self._calculate_profitability_ratios(financial_data)
        
        # Liquidity Ratios
        ratios["liquidity"] = self._calculate_liquidity_ratios(financial_data)
        
        # Efficiency Ratios
        ratios["efficiency"] = self._calculate_efficiency_ratios(financial_data)
        
        # Leverage Ratios
        ratios["leverage"] = self._calculate_leverage_ratios(financial_data)
        
        # Growth Ratios (if historical data available)
        if financial_data.get("historical_data"):
            ratios["growth"] = self._calculate_growth_ratios(financial_data)
        
        return ratios
    
    def _calculate_profitability_ratios(self, data: Dict[str, Any]) -> Dict[str, float]:
        """Calculate profitability ratios"""
        revenue = data.get("total_revenue", 0)
        expenses = data.get("total_expenses", 0)
        net_profit = data.get("net_profit", revenue - expenses)
        gross_profit = data.get("gross_profit", net_profit)
        assets = data.get("total_assets", 1)
        equity = data.get("equity", 1)
        
        return {
            "gross_profit_margin": (gross_profit / revenue * 100) if revenue > 0 else 0,
            "net_profit_margin": (net_profit / revenue * 100) if revenue > 0 else 0,
            "return_on_assets": (net_profit / assets * 100) if assets > 0 else 0,
            "return_on_equity": (net_profit / equity * 100) if equity > 0 else 0,
        }
    
    def _calculate_liquidity_ratios(self, data: Dict[str, Any]) -> Dict[str, float]:
        """Calculate liquidity ratios"""
        current_assets = data.get("current_assets", data.get("cash_balance", 0) + data.get("accounts_receivable", 0))
        current_liabilities = data.get("current_liabilities", data.get("accounts_payable", 0))
        cash = data.get("cash_balance", 0)
        inventory = data.get("inventory_value", 0)
        
        return {
            "current_ratio": (current_assets / current_liabilities) if current_liabilities > 0 else 0,
            "quick_ratio": ((current_assets - inventory) / current_liabilities) if current_liabilities > 0 else 0,
            "cash_ratio": (cash / current_liabilities) if current_liabilities > 0 else 0,
        }
    
    def _calculate_efficiency_ratios(self, data: Dict[str, Any]) -> Dict[str, float]:
        """Calculate efficiency ratios"""
        revenue = data.get("total_revenue", 0)
        assets = data.get("total_assets", 1)
        receivables = data.get("accounts_receivable", 0)
        payables = data.get("accounts_payable", 0)
        inventory = data.get("inventory_value", 0)
        cogs = data.get("cost_of_goods_sold", data.get("total_expenses", 0) * 0.7)  # Estimate if not provided
        
        return {
            "asset_turnover": (revenue / assets) if assets > 0 else 0,
            "receivables_turnover": (revenue / receivables) if receivables > 0 else 0,
            "days_sales_outstanding": (receivables / (revenue / 365)) if revenue > 0 else 0,
            "inventory_turnover": (cogs / inventory) if inventory > 0 else 0,
            "days_inventory_outstanding": (inventory / (cogs / 365)) if cogs > 0 else 0,
        }
    
    def _calculate_leverage_ratios(self, data: Dict[str, Any]) -> Dict[str, float]:
        """Calculate leverage/solvency ratios"""
        assets = data.get("total_assets", 0)
        liabilities = data.get("total_liabilities", 0)
        equity = data.get("equity", assets - liabilities)
        ebit = data.get("ebit", data.get("net_profit", 0))
        interest = data.get("interest_expense", 0)
        
        return {
            "debt_to_equity": (liabilities / equity) if equity > 0 else 0,
            "debt_to_assets": (liabilities / assets) if assets > 0 else 0,
            "equity_ratio": (equity / assets) if assets > 0 else 0,
            "interest_coverage": (ebit / interest) if interest > 0 else 999,  # High number if no interest
        }
    
    def _calculate_growth_ratios(self, data: Dict[str, Any]) -> Dict[str, float]:
        """Calculate growth rates"""
        historical = data.get("historical_data", [])
        if len(historical) < 2:
            return {}
        
        # Revenue growth
        revenue_growth = self._calculate_growth_rate(
            [h.get("revenue", 0) for h in historical]
        )
        
        # Profit growth
        profit_growth = self._calculate_growth_rate(
            [h.get("net_profit", 0) for h in historical]
        )
        
        return {
            "revenue_growth_rate": revenue_growth,
            "profit_growth_rate": profit_growth,
        }
    
    def _calculate_growth_rate(self, values: List[float]) -> float:
        """Calculate average growth rate"""
        if len(values) < 2:
            return 0
        
        growth_rates = []
        for i in range(1, len(values)):
            if values[i-1] > 0:
                growth = ((values[i] - values[i-1]) / values[i-1]) * 100
                growth_rates.append(growth)
        
        return statistics.mean(growth_rates) if growth_rates else 0
    
    def calculate_health_score(self, financial_data: Dict[str, Any], ratios: Dict[str, Any]) -> float:
        """Calculate overall financial health score (0-100)"""
        score = 0
        max_score = 100
        
        # Profitability (30 points)
        prof = ratios.get("profitability", {})
        npm = prof.get("net_profit_margin", 0)
        if npm > 20:
            score += 30
        elif npm > 10:
            score += 20
        elif npm > 5:
            score += 15
        elif npm > 0:
            score += 10
        
        # Liquidity (25 points)
        liq = ratios.get("liquidity", {})
        current_ratio = liq.get("current_ratio", 0)
        if current_ratio >= 2:
            score += 25
        elif current_ratio >= 1.5:
            score += 20
        elif current_ratio >= 1:
            score += 15
        elif current_ratio >= 0.5:
            score += 10
        
        # Leverage (20 points)
        lev = ratios.get("leverage", {})
        debt_to_equity = lev.get("debt_to_equity", 0)
        if debt_to_equity < 0.5:
            score += 20
        elif debt_to_equity < 1:
            score += 15
        elif debt_to_equity < 2:
            score += 10
        elif debt_to_equity < 3:
            score += 5
        
        # Efficiency (15 points)
        eff = ratios.get("efficiency", {})
        asset_turnover = eff.get("asset_turnover", 0)
        if asset_turnover > 2:
            score += 15
        elif asset_turnover > 1:
            score += 12
        elif asset_turnover > 0.5:
            score += 8
        
        # Growth (10 points)
        growth = ratios.get("growth", {})
        revenue_growth = growth.get("revenue_growth_rate", 0)
        if revenue_growth > 20:
            score += 10
        elif revenue_growth > 10:
            score += 8
        elif revenue_growth > 5:
            score += 6
        elif revenue_growth > 0:
            score += 4
        
        return min(score, max_score)
    
    def calculate_credit_score(self, financial_data: Dict[str, Any], ratios: Dict[str, Any]) -> int:
        """Calculate credit score (300-900)"""
        base_score = 300
        max_score = 900
        
        # Payment history (35% weight)
        payment_score = 210  # Assume good if no data
        
        # Debt utilization (30% weight)
        lev = ratios.get("leverage", {})
        debt_to_equity = lev.get("debt_to_equity", 0)
        if debt_to_equity < 0.3:
            utilization_score = 180
        elif debt_to_equity < 0.5:
            utilization_score = 150
        elif debt_to_equity < 1:
            utilization_score = 120
        elif debt_to_equity < 2:
            utilization_score = 90
        else:
            utilization_score = 60
        
        # Profitability (20% weight)
        prof = ratios.get("profitability", {})
        npm = prof.get("net_profit_margin", 0)
        if npm > 15:
            profit_score = 120
        elif npm > 10:
            profit_score = 100
        elif npm > 5:
            profit_score = 80
        elif npm > 0:
            profit_score = 60
        else:
            profit_score = 30
        
        # Cash flow (15% weight)
        liq = ratios.get("liquidity", {})
        current_ratio = liq.get("current_ratio", 0)
        if current_ratio > 2:
            cash_score = 90
        elif current_ratio > 1.5:
            cash_score = 75
        elif current_ratio > 1:
            cash_score = 60
        else:
            cash_score = 30
        
        total_score = base_score + payment_score + utilization_score + profit_score + cash_score
        return min(int(total_score), max_score)
    
    def assess_risk_level(self, financial_data: Dict[str, Any], ratios: Dict[str, Any]) -> Dict[str, Any]:
        """Assess overall risk level"""
        risk_factors = []
        risk_score = 0
        
        # Check profitability
        prof = ratios.get("profitability", {})
        if prof.get("net_profit_margin", 0) < 0:
            risk_factors.append("Negative profit margins")
            risk_score += 30
        elif prof.get("net_profit_margin", 0) < 5:
            risk_factors.append("Low profit margins")
            risk_score += 15
        
        # Check liquidity
        liq = ratios.get("liquidity", {})
        if liq.get("current_ratio", 0) < 1:
            risk_factors.append("Liquidity concerns - current ratio below 1")
            risk_score += 25
        elif liq.get("current_ratio", 0) < 1.5:
            risk_factors.append("Moderate liquidity - current ratio below 1.5")
            risk_score += 10
        
        # Check leverage
        lev = ratios.get("leverage", {})
        if lev.get("debt_to_equity", 0) > 3:
            risk_factors.append("Very high debt levels")
            risk_score += 30
        elif lev.get("debt_to_equity", 0) > 2:
            risk_factors.append("High debt levels")
            risk_score += 20
        
        # Check cash position
        cash_balance = financial_data.get("cash_balance", 0)
        monthly_expenses = financial_data.get("total_expenses", 0) / 12
        if monthly_expenses > 0 and (cash_balance / monthly_expenses) < 1:
            risk_factors.append("Low cash reserves (less than 1 month of expenses)")
            risk_score += 20
        
        # Determine risk level
        if risk_score >= 60:
            risk_level = "high"
        elif risk_score >= 30:
            risk_level = "medium"
        else:
            risk_level = "low"
        
        return {
            "risk_level": risk_level,
            "risk_score": risk_score,
            "risk_factors": risk_factors,
            "recommendations": self._get_risk_mitigation_recommendations(risk_factors)
        }
    
    def _get_risk_mitigation_recommendations(self, risk_factors: List[str]) -> List[str]:
        """Generate risk mitigation recommendations"""
        recommendations = []
        
        for factor in risk_factors:
            if "profit" in factor.lower():
                recommendations.append("Focus on cost reduction and revenue optimization")
            if "liquidity" in factor.lower():
                recommendations.append("Improve cash collection and consider short-term financing")
            if "debt" in factor.lower():
                recommendations.append("Develop debt reduction plan and avoid new borrowings")
            if "cash" in factor.lower():
                recommendations.append("Build emergency cash reserves - target 3-6 months expenses")
        
        return list(set(recommendations))  # Remove duplicates
    
    def benchmark_against_industry(self, ratios: Dict[str, Any], industry: str) -> Dict[str, Any]:
        """Compare ratios against industry benchmarks"""
        benchmarks = self.industry_benchmarks.get(industry, self.industry_benchmarks.get("general", {}))
        
        comparison = {}
        
        for category, ratios_dict in ratios.items():
            comparison[category] = {}
            for ratio_name, ratio_value in ratios_dict.items():
                benchmark_value = benchmarks.get(category, {}).get(ratio_name)
                if benchmark_value:
                    comparison[category][ratio_name] = {
                        "value": ratio_value,
                        "benchmark": benchmark_value,
                        "difference": ratio_value - benchmark_value,
                        "performance": "above" if ratio_value > benchmark_value else "below"
                    }
        
        return comparison
    
    def _load_industry_benchmarks(self) -> Dict[str, Any]:
        """Load industry benchmark data"""
        # This would typically come from a database or external source
        return {
            "manufacturing": {
                "profitability": {"net_profit_margin": 8.5, "return_on_assets": 6.2},
                "liquidity": {"current_ratio": 1.5, "quick_ratio": 1.0},
                "leverage": {"debt_to_equity": 1.2, "debt_to_assets": 0.45},
                "efficiency": {"asset_turnover": 1.2}
            },
            "retail": {
                "profitability": {"net_profit_margin": 5.2, "return_on_assets": 7.5},
                "liquidity": {"current_ratio": 1.8, "quick_ratio": 0.8},
                "leverage": {"debt_to_equity": 0.8, "debt_to_assets": 0.38},
                "efficiency": {"asset_turnover": 2.5}
            },
            "services": {
                "profitability": {"net_profit_margin": 12.5, "return_on_assets": 15.2},
                "liquidity": {"current_ratio": 2.0, "quick_ratio": 1.8},
                "leverage": {"debt_to_equity": 0.5, "debt_to_assets": 0.25},
                "efficiency": {"asset_turnover": 1.8}
            },
            "general": {
                "profitability": {"net_profit_margin": 10.0, "return_on_assets": 8.0},
                "liquidity": {"current_ratio": 1.5, "quick_ratio": 1.0},
                "leverage": {"debt_to_equity": 1.0, "debt_to_assets": 0.4},
                "efficiency": {"asset_turnover": 1.5}
            }
        }

# Singleton instance
financial_calculator = FinancialCalculator()
