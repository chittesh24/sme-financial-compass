"""
Data processing service for CSV, Excel, and other formats
"""
import pandas as pd
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
import io

logger = logging.getLogger(__name__)

class DataProcessor:
    """Process uploaded financial data files"""
    
    def __init__(self):
        self.date_formats = [
            '%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y', '%d-%m-%Y',
            '%Y/%m/%d', '%d.%m.%Y', '%Y.%m.%d'
        ]
    
    def parse_csv(self, file_content: bytes) -> Dict[str, Any]:
        """Parse CSV file"""
        try:
            df = pd.read_csv(io.BytesIO(file_content))
            return self._process_dataframe(df, 'csv')
        except Exception as e:
            logger.error(f"CSV parsing error: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def parse_excel(self, file_content: bytes) -> Dict[str, Any]:
        """Parse Excel file (xlsx, xls)"""
        try:
            # Try to read all sheets
            excel_file = pd.ExcelFile(io.BytesIO(file_content))
            sheets = {}
            
            for sheet_name in excel_file.sheet_names:
                df = pd.read_excel(excel_file, sheet_name=sheet_name)
                sheets[sheet_name] = self._process_dataframe(df, f'excel_{sheet_name}')
            
            # If only one sheet, return it directly
            if len(sheets) == 1:
                return list(sheets.values())[0]
            
            # Otherwise, try to intelligently combine or return all sheets
            return {
                "success": True,
                "sheets": sheets,
                "source": "excel"
            }
            
        except Exception as e:
            logger.error(f"Excel parsing error: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def _process_dataframe(self, df: pd.DataFrame, source: str) -> Dict[str, Any]:
        """Process pandas DataFrame into structured financial data"""
        try:
            # Clean column names
            df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
            
            # Detect data type
            data_type = self._detect_data_type(df)
            
            if data_type == 'profit_loss':
                return self._process_profit_loss(df, source)
            elif data_type == 'balance_sheet':
                return self._process_balance_sheet(df, source)
            elif data_type == 'cashflow':
                return self._process_cashflow(df, source)
            elif data_type == 'transactions':
                return self._process_transactions(df, source)
            else:
                # Generic processing
                return self._process_generic(df, source)
                
        except Exception as e:
            logger.error(f"DataFrame processing error: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def _detect_data_type(self, df: pd.DataFrame) -> str:
        """Detect the type of financial data"""
        columns = [col.lower() for col in df.columns]
        
        # Profit & Loss indicators
        pl_keywords = ['revenue', 'sales', 'income', 'expense', 'profit', 'loss', 'cost']
        pl_score = sum(1 for col in columns if any(kw in col for kw in pl_keywords))
        
        # Balance Sheet indicators
        bs_keywords = ['asset', 'liability', 'equity', 'capital', 'receivable', 'payable']
        bs_score = sum(1 for col in columns if any(kw in col for kw in bs_keywords))
        
        # Cashflow indicators
        cf_keywords = ['cash', 'flow', 'inflow', 'outflow', 'operating', 'investing', 'financing']
        cf_score = sum(1 for col in columns if any(kw in col for kw in cf_keywords))
        
        # Transaction indicators
        txn_keywords = ['transaction', 'date', 'amount', 'description', 'category', 'debit', 'credit']
        txn_score = sum(1 for col in columns if any(kw in col for kw in txn_keywords))
        
        scores = {
            'profit_loss': pl_score,
            'balance_sheet': bs_score,
            'cashflow': cf_score,
            'transactions': txn_score
        }
        
        return max(scores, key=scores.get) if max(scores.values()) > 0 else 'unknown'
    
    def _process_profit_loss(self, df: pd.DataFrame, source: str) -> Dict[str, Any]:
        """Process Profit & Loss statement"""
        try:
            result = {
                "success": True,
                "data_type": "profit_loss",
                "source": source,
                "periods": []
            }
            
            # Find date/period column
            date_col = self._find_column(df, ['date', 'period', 'month', 'year'])
            
            # Find revenue columns
            revenue_col = self._find_column(df, ['revenue', 'sales', 'income', 'turnover'])
            expense_col = self._find_column(df, ['expense', 'expenses', 'cost', 'expenditure'])
            
            if date_col and (revenue_col or expense_col):
                for _, row in df.iterrows():
                    period_data = {
                        "period": str(row[date_col]),
                        "revenue": self._safe_float(row.get(revenue_col, 0)),
                        "expenses": self._safe_float(row.get(expense_col, 0)),
                    }
                    period_data['profit'] = period_data['revenue'] - period_data['expenses']
                    result['periods'].append(period_data)
            
            # Calculate summary
            if result['periods']:
                result['summary'] = {
                    "total_revenue": sum(p['revenue'] for p in result['periods']),
                    "total_expenses": sum(p['expenses'] for p in result['periods']),
                    "net_profit": sum(p['profit'] for p in result['periods']),
                    "period_count": len(result['periods'])
                }
            
            return result
            
        except Exception as e:
            logger.error(f"P&L processing error: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def _process_balance_sheet(self, df: pd.DataFrame, source: str) -> Dict[str, Any]:
        """Process Balance Sheet"""
        try:
            result = {
                "success": True,
                "data_type": "balance_sheet",
                "source": source,
                "data": {}
            }
            
            # Find key columns
            assets_col = self._find_column(df, ['assets', 'total_assets'])
            liabilities_col = self._find_column(df, ['liabilities', 'total_liabilities'])
            equity_col = self._find_column(df, ['equity', 'capital', 'net_worth'])
            
            if assets_col:
                result['data']['total_assets'] = self._safe_float(df[assets_col].sum())
            if liabilities_col:
                result['data']['total_liabilities'] = self._safe_float(df[liabilities_col].sum())
            if equity_col:
                result['data']['equity'] = self._safe_float(df[equity_col].sum())
            
            # Calculate derived values
            if 'total_assets' in result['data'] and 'total_liabilities' in result['data']:
                result['data']['calculated_equity'] = result['data']['total_assets'] - result['data']['total_liabilities']
            
            return result
            
        except Exception as e:
            logger.error(f"Balance sheet processing error: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def _process_cashflow(self, df: pd.DataFrame, source: str) -> Dict[str, Any]:
        """Process Cash Flow statement"""
        try:
            result = {
                "success": True,
                "data_type": "cashflow",
                "source": source,
                "periods": []
            }
            
            date_col = self._find_column(df, ['date', 'period', 'month'])
            inflow_col = self._find_column(df, ['inflow', 'cash_in', 'receipts'])
            outflow_col = self._find_column(df, ['outflow', 'cash_out', 'payments'])
            
            if date_col and (inflow_col or outflow_col):
                for _, row in df.iterrows():
                    period_data = {
                        "period": str(row[date_col]),
                        "inflow": self._safe_float(row.get(inflow_col, 0)),
                        "outflow": self._safe_float(row.get(outflow_col, 0)),
                    }
                    period_data['net_cashflow'] = period_data['inflow'] - period_data['outflow']
                    result['periods'].append(period_data)
            
            return result
            
        except Exception as e:
            logger.error(f"Cashflow processing error: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def _process_transactions(self, df: pd.DataFrame, source: str) -> Dict[str, Any]:
        """Process transaction data"""
        try:
            result = {
                "success": True,
                "data_type": "transactions",
                "source": source,
                "transactions": [],
                "summary": {}
            }
            
            date_col = self._find_column(df, ['date', 'transaction_date', 'txn_date'])
            amount_col = self._find_column(df, ['amount', 'value', 'debit', 'credit'])
            desc_col = self._find_column(df, ['description', 'narration', 'details', 'particulars'])
            category_col = self._find_column(df, ['category', 'type', 'class'])
            
            for _, row in df.iterrows():
                txn = {
                    "date": str(row[date_col]) if date_col else None,
                    "amount": self._safe_float(row.get(amount_col, 0)),
                    "description": str(row[desc_col]) if desc_col and pd.notna(row.get(desc_col)) else "",
                    "category": str(row[category_col]) if category_col and pd.notna(row.get(category_col)) else "Uncategorized"
                }
                result['transactions'].append(txn)
            
            # Calculate summary
            if result['transactions']:
                result['summary'] = {
                    "total_transactions": len(result['transactions']),
                    "total_amount": sum(t['amount'] for t in result['transactions']),
                    "categories": list(set(t['category'] for t in result['transactions']))
                }
            
            return result
            
        except Exception as e:
            logger.error(f"Transaction processing error: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def _process_generic(self, df: pd.DataFrame, source: str) -> Dict[str, Any]:
        """Generic processing for unknown data formats"""
        try:
            return {
                "success": True,
                "data_type": "generic",
                "source": source,
                "columns": list(df.columns),
                "row_count": len(df),
                "sample_data": df.head(10).to_dict('records'),
                "summary": df.describe().to_dict() if len(df) > 0 else {}
            }
        except Exception as e:
            logger.error(f"Generic processing error: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def _find_column(self, df: pd.DataFrame, keywords: List[str]) -> Optional[str]:
        """Find column matching keywords"""
        columns = [col.lower() for col in df.columns]
        for keyword in keywords:
            for col in df.columns:
                if keyword in col.lower():
                    return col
        return None
    
    def _safe_float(self, value: Any) -> float:
        """Safely convert value to float"""
        try:
            if pd.isna(value):
                return 0.0
            # Remove currency symbols and commas
            if isinstance(value, str):
                value = value.replace('₹', '').replace('$', '').replace(',', '').strip()
            return float(value)
        except (ValueError, TypeError):
            return 0.0

# Singleton instance
data_processor = DataProcessor()
