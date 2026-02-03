"""
Database connection and schema management using Supabase
"""
from supabase import create_client, Client
from app.config import settings
import logging
from typing import Optional

logger = logging.getLogger(__name__)

# Supabase client
supabase: Optional[Client] = None

def get_supabase() -> Client:
    """Get Supabase client instance"""
    global supabase
    if supabase is None:
        if not settings.SUPABASE_URL or not settings.SUPABASE_SERVICE_KEY:
            raise ValueError("Supabase credentials not configured")
        supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_KEY)
    return supabase

async def init_db():
    """Initialize database connection and create tables if needed"""
    try:
        client = get_supabase()
        logger.info("Database connection established successfully")
        # Test connection
        response = client.table('businesses').select("id").limit(1).execute()
        logger.info("Database tables verified")
    except Exception as e:
        logger.error(f"Database initialization error: {str(e)}")
        logger.warning("Continuing without database - some features may not work")

# Database schema SQL (to be run in Supabase SQL editor)
SCHEMA_SQL = """
-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Businesses table
CREATE TABLE IF NOT EXISTS businesses (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL,
    business_name VARCHAR(255) NOT NULL,
    industry VARCHAR(100) NOT NULL,
    registration_number VARCHAR(100),
    gst_number VARCHAR(20),
    pan_number VARCHAR(10),
    address TEXT,
    city VARCHAR(100),
    state VARCHAR(100),
    country VARCHAR(100) DEFAULT 'India',
    annual_revenue DECIMAL(15, 2),
    employee_count INTEGER,
    established_date DATE,
    business_type VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Financial data table
CREATE TABLE IF NOT EXISTS financial_data (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    business_id UUID NOT NULL REFERENCES businesses(id) ON DELETE CASCADE,
    period_start DATE NOT NULL,
    period_end DATE NOT NULL,
    total_revenue DECIMAL(15, 2),
    total_expenses DECIMAL(15, 2),
    gross_profit DECIMAL(15, 2),
    net_profit DECIMAL(15, 2),
    accounts_receivable DECIMAL(15, 2),
    accounts_payable DECIMAL(15, 2),
    inventory_value DECIMAL(15, 2),
    cash_balance DECIMAL(15, 2),
    total_assets DECIMAL(15, 2),
    total_liabilities DECIMAL(15, 2),
    equity DECIMAL(15, 2),
    data_source VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Uploaded documents table
CREATE TABLE IF NOT EXISTS uploaded_documents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    business_id UUID NOT NULL REFERENCES businesses(id) ON DELETE CASCADE,
    file_name VARCHAR(255) NOT NULL,
    file_type VARCHAR(50) NOT NULL,
    file_size INTEGER,
    file_path TEXT,
    upload_status VARCHAR(50) DEFAULT 'pending',
    processed_at TIMESTAMP,
    extracted_data JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Financial analysis results
CREATE TABLE IF NOT EXISTS analysis_results (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    business_id UUID NOT NULL REFERENCES businesses(id) ON DELETE CASCADE,
    analysis_type VARCHAR(100) NOT NULL,
    health_score DECIMAL(5, 2),
    credit_score DECIMAL(5, 2),
    risk_level VARCHAR(50),
    insights JSONB,
    recommendations JSONB,
    financial_ratios JSONB,
    benchmarks JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Forecasts table
CREATE TABLE IF NOT EXISTS forecasts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    business_id UUID NOT NULL REFERENCES businesses(id) ON DELETE CASCADE,
    forecast_type VARCHAR(50) NOT NULL,
    forecast_period VARCHAR(50) NOT NULL,
    forecast_data JSONB NOT NULL,
    confidence_level DECIMAL(5, 2),
    methodology VARCHAR(100),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Reports table
CREATE TABLE IF NOT EXISTS reports (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    business_id UUID NOT NULL REFERENCES businesses(id) ON DELETE CASCADE,
    report_type VARCHAR(100) NOT NULL,
    report_name VARCHAR(255) NOT NULL,
    report_data JSONB,
    file_path TEXT,
    language VARCHAR(10) DEFAULT 'en',
    created_at TIMESTAMP DEFAULT NOW()
);

-- Banking connections
CREATE TABLE IF NOT EXISTS banking_connections (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    business_id UUID NOT NULL REFERENCES businesses(id) ON DELETE CASCADE,
    provider VARCHAR(50) NOT NULL,
    institution_name VARCHAR(255),
    account_id VARCHAR(255),
    access_token_encrypted TEXT,
    connection_status VARCHAR(50) DEFAULT 'active',
    last_sync TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Banking transactions
CREATE TABLE IF NOT EXISTS banking_transactions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    connection_id UUID NOT NULL REFERENCES banking_connections(id) ON DELETE CASCADE,
    transaction_id VARCHAR(255) NOT NULL,
    transaction_date DATE NOT NULL,
    amount DECIMAL(15, 2) NOT NULL,
    currency VARCHAR(10) DEFAULT 'INR',
    description TEXT,
    category VARCHAR(100),
    transaction_type VARCHAR(50),
    balance DECIMAL(15, 2),
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(connection_id, transaction_id)
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_businesses_user_id ON businesses(user_id);
CREATE INDEX IF NOT EXISTS idx_financial_data_business_id ON financial_data(business_id);
CREATE INDEX IF NOT EXISTS idx_financial_data_period ON financial_data(period_start, period_end);
CREATE INDEX IF NOT EXISTS idx_uploaded_documents_business_id ON uploaded_documents(business_id);
CREATE INDEX IF NOT EXISTS idx_analysis_results_business_id ON analysis_results(business_id);
CREATE INDEX IF NOT EXISTS idx_forecasts_business_id ON forecasts(business_id);
CREATE INDEX IF NOT EXISTS idx_reports_business_id ON reports(business_id);
CREATE INDEX IF NOT EXISTS idx_banking_connections_business_id ON banking_connections(business_id);
CREATE INDEX IF NOT EXISTS idx_banking_transactions_connection_id ON banking_transactions(connection_id);
CREATE INDEX IF NOT EXISTS idx_banking_transactions_date ON banking_transactions(transaction_date);

-- Enable Row Level Security
ALTER TABLE businesses ENABLE ROW LEVEL SECURITY;
ALTER TABLE financial_data ENABLE ROW LEVEL SECURITY;
ALTER TABLE uploaded_documents ENABLE ROW LEVEL SECURITY;
ALTER TABLE analysis_results ENABLE ROW LEVEL SECURITY;
ALTER TABLE forecasts ENABLE ROW LEVEL SECURITY;
ALTER TABLE reports ENABLE ROW LEVEL SECURITY;
ALTER TABLE banking_connections ENABLE ROW LEVEL SECURITY;
ALTER TABLE banking_transactions ENABLE ROW LEVEL SECURITY;
"""
