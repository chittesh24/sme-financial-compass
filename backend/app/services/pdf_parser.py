"""
PDF parsing service for financial documents
"""
import pdfplumber
import PyPDF2
import logging
from typing import Dict, Any, List, Optional
import io
import re
from datetime import datetime

logger = logging.getLogger(__name__)

class PDFParser:
    """Parse PDF financial documents"""
    
    def __init__(self):
        self.currency_pattern = re.compile(r'[₹$€£]\s*[\d,]+\.?\d*')
        self.number_pattern = re.compile(r'[\d,]+\.?\d*')
        self.date_patterns = [
            r'\d{2}/\d{2}/\d{4}',
            r'\d{2}-\d{2}-\d{4}',
            r'\d{4}-\d{2}-\d{2}'
        ]
    
    def parse_pdf(self, file_content: bytes) -> Dict[str, Any]:
        """Main PDF parsing method"""
        try:
            # Try pdfplumber first (better for tables)
            result = self._parse_with_pdfplumber(file_content)
            if result.get('success'):
                return result
            
            # Fall back to PyPDF2
            logger.info("Falling back to PyPDF2")
            return self._parse_with_pypdf2(file_content)
            
        except Exception as e:
            logger.error(f"PDF parsing error: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _parse_with_pdfplumber(self, file_content: bytes) -> Dict[str, Any]:
        """Parse PDF using pdfplumber (better for structured data)"""
        try:
            with pdfplumber.open(io.BytesIO(file_content)) as pdf:
                result = {
                    "success": True,
                    "num_pages": len(pdf.pages),
                    "text": "",
                    "tables": [],
                    "financial_data": {},
                    "metadata": {}
                }
                
                # Extract text and tables from each page
                for page_num, page in enumerate(pdf.pages, 1):
                    # Extract text
                    page_text = page.extract_text()
                    if page_text:
                        result["text"] += f"\n--- Page {page_num} ---\n{page_text}"
                    
                    # Extract tables
                    tables = page.extract_tables()
                    for table_num, table in enumerate(tables):
                        if table:
                            result["tables"].append({
                                "page": page_num,
                                "table_number": table_num + 1,
                                "data": table
                            })
                
                # Analyze extracted data
                result["financial_data"] = self._extract_financial_data(result["text"], result["tables"])
                result["metadata"] = pdf.metadata
                
                return result
                
        except Exception as e:
            logger.error(f"pdfplumber parsing error: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def _parse_with_pypdf2(self, file_content: bytes) -> Dict[str, Any]:
        """Parse PDF using PyPDF2 (fallback)"""
        try:
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_content))
            
            result = {
                "success": True,
                "num_pages": len(pdf_reader.pages),
                "text": "",
                "financial_data": {},
                "metadata": {}
            }
            
            # Extract text from all pages
            for page_num, page in enumerate(pdf_reader.pages, 1):
                page_text = page.extract_text()
                if page_text:
                    result["text"] += f"\n--- Page {page_num} ---\n{page_text}"
            
            # Extract financial data from text
            result["financial_data"] = self._extract_financial_data(result["text"], [])
            result["metadata"] = pdf_reader.metadata
            
            return result
            
        except Exception as e:
            logger.error(f"PyPDF2 parsing error: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def _extract_financial_data(self, text: str, tables: List[Dict]) -> Dict[str, Any]:
        """Extract financial data from text and tables"""
        financial_data = {
            "detected_amounts": [],
            "detected_dates": [],
            "key_metrics": {},
            "document_type": self._detect_document_type(text)
        }
        
        # Extract amounts
        amounts = self.currency_pattern.findall(text)
        financial_data["detected_amounts"] = [self._parse_amount(amt) for amt in amounts]
        
        # Extract dates
        for pattern in self.date_patterns:
            dates = re.findall(pattern, text)
            financial_data["detected_dates"].extend(dates)
        
        # Look for specific financial terms
        terms = {
            "revenue": ["revenue", "sales", "income", "turnover"],
            "expenses": ["expense", "expenditure", "cost"],
            "profit": ["profit", "net income", "earnings"],
            "loss": ["loss", "deficit"],
            "assets": ["assets", "total assets"],
            "liabilities": ["liabilities", "total liabilities"],
            "equity": ["equity", "net worth", "capital"]
        }
        
        for key, keywords in terms.items():
            for keyword in keywords:
                pattern = f"{keyword}[:\\s]+{self.currency_pattern.pattern}"
                matches = re.finditer(pattern, text, re.IGNORECASE)
                for match in matches:
                    amount_str = re.search(self.currency_pattern, match.group())
                    if amount_str:
                        financial_data["key_metrics"][key] = self._parse_amount(amount_str.group())
                        break
        
        # Process tables if available
        if tables:
            financial_data["table_data"] = self._process_tables(tables)
        
        return financial_data
    
    def _detect_document_type(self, text: str) -> str:
        """Detect type of financial document"""
        text_lower = text.lower()
        
        if any(term in text_lower for term in ["profit and loss", "p&l", "income statement"]):
            return "profit_loss"
        elif any(term in text_lower for term in ["balance sheet", "statement of financial position"]):
            return "balance_sheet"
        elif any(term in text_lower for term in ["cash flow", "cashflow", "statement of cash flows"]):
            return "cashflow"
        elif any(term in text_lower for term in ["bank statement", "account statement"]):
            return "bank_statement"
        elif any(term in text_lower for term in ["invoice", "bill"]):
            return "invoice"
        elif any(term in text_lower for term in ["gst", "tax return", "tax statement"]):
            return "tax_document"
        else:
            return "unknown"
    
    def _parse_amount(self, amount_str: str) -> float:
        """Parse amount string to float"""
        try:
            # Remove currency symbols and commas
            cleaned = re.sub(r'[₹$€£,\s]', '', amount_str)
            return float(cleaned)
        except (ValueError, TypeError):
            return 0.0
    
    def _process_tables(self, tables: List[Dict]) -> List[Dict[str, Any]]:
        """Process extracted tables"""
        processed_tables = []
        
        for table_info in tables:
            table_data = table_info.get("data", [])
            if not table_data or len(table_data) < 2:
                continue
            
            # Assume first row is header
            headers = table_data[0]
            rows = table_data[1:]
            
            # Convert to list of dicts
            table_records = []
            for row in rows:
                if len(row) == len(headers):
                    record = {str(headers[i]).strip(): row[i] for i in range(len(headers)) if row[i]}
                    table_records.append(record)
            
            if table_records:
                processed_tables.append({
                    "page": table_info.get("page"),
                    "table_number": table_info.get("table_number"),
                    "records": table_records
                })
        
        return processed_tables
    
    def extract_bank_statement_data(self, file_content: bytes) -> Dict[str, Any]:
        """Specialized extraction for bank statements"""
        result = self.parse_pdf(file_content)
        
        if not result.get("success"):
            return result
        
        transactions = []
        
        # Try to extract from tables first
        if result.get("tables"):
            for table_info in result["tables"]:
                table_data = table_info.get("data", [])
                if len(table_data) > 1:
                    # Look for date, description, amount columns
                    for row in table_data[1:]:
                        if len(row) >= 3:
                            try:
                                txn = {
                                    "date": row[0],
                                    "description": row[1] if len(row) > 1 else "",
                                    "amount": self._parse_amount(row[-1]) if row[-1] else 0
                                }
                                transactions.append(txn)
                            except:
                                continue
        
        return {
            "success": True,
            "document_type": "bank_statement",
            "transactions": transactions,
            "transaction_count": len(transactions),
            "total_amount": sum(t["amount"] for t in transactions)
        }
    
    def extract_gst_data(self, file_content: bytes) -> Dict[str, Any]:
        """Specialized extraction for GST documents"""
        result = self.parse_pdf(file_content)
        
        if not result.get("success"):
            return result
        
        text = result.get("text", "")
        
        # Extract GSTIN
        gstin_pattern = r'\d{2}[A-Z]{5}\d{4}[A-Z]{1}[A-Z\d]{1}[Z]{1}[A-Z\d]{1}'
        gstin_matches = re.findall(gstin_pattern, text)
        
        # Extract tax amounts
        tax_data = {
            "gstin": gstin_matches[0] if gstin_matches else None,
            "cgst": 0,
            "sgst": 0,
            "igst": 0,
            "total_tax": 0
        }
        
        # Look for tax amounts
        cgst_match = re.search(r'cgst[:\s]+[\d,]+\.?\d*', text, re.IGNORECASE)
        if cgst_match:
            tax_data["cgst"] = self._parse_amount(re.search(self.number_pattern, cgst_match.group()).group())
        
        sgst_match = re.search(r'sgst[:\s]+[\d,]+\.?\d*', text, re.IGNORECASE)
        if sgst_match:
            tax_data["sgst"] = self._parse_amount(re.search(self.number_pattern, sgst_match.group()).group())
        
        igst_match = re.search(r'igst[:\s]+[\d,]+\.?\d*', text, re.IGNORECASE)
        if igst_match:
            tax_data["igst"] = self._parse_amount(re.search(self.number_pattern, igst_match.group()).group())
        
        tax_data["total_tax"] = tax_data["cgst"] + tax_data["sgst"] + tax_data["igst"]
        
        return {
            "success": True,
            "document_type": "gst_document",
            "tax_data": tax_data
        }

# Singleton instance
pdf_parser = PDFParser()
