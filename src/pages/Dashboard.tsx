import { DashboardLayout } from "@/components/layout/DashboardLayout";
import { MetricCard } from "@/components/dashboard/MetricCard";
import { HealthScoreGauge } from "@/components/dashboard/HealthScoreGauge";
import { RiskIndicator } from "@/components/dashboard/RiskIndicator";
import { RevenueChart } from "@/components/dashboard/RevenueChart";
import { ExpenseBreakdown } from "@/components/dashboard/ExpenseBreakdown";
import { InsightCard } from "@/components/dashboard/InsightCard";
import {
  IndianRupee,
  TrendingUp,
  CreditCard,
  Wallet,
  ArrowUpRight,
  ArrowDownRight,
} from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { useNavigate } from "react-router-dom";

// Sample data for demonstration
const revenueData = [
  { month: "Jan", revenue: 1200000, expenses: 900000 },
  { month: "Feb", revenue: 1350000, expenses: 950000 },
  { month: "Mar", revenue: 1100000, expenses: 880000 },
  { month: "Apr", revenue: 1450000, expenses: 1020000 },
  { month: "May", revenue: 1600000, expenses: 1100000 },
  { month: "Jun", revenue: 1750000, expenses: 1150000 },
];

const expenseData = [
  { name: "Salaries", value: 450000 },
  { name: "Operations", value: 280000 },
  { name: "Marketing", value: 150000 },
  { name: "Inventory", value: 180000 },
  { name: "Others", value: 90000 },
];

export default function Dashboard() {
  const navigate = useNavigate();

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold tracking-tight">Financial Dashboard</h1>
            <p className="text-muted-foreground">
              Welcome back! Here's your business financial overview.
            </p>
          </div>
          <Button onClick={() => navigate("/upload")} className="gap-2">
            <ArrowUpRight className="h-4 w-4" />
            Upload New Data
          </Button>
        </div>

        {/* Key Metrics */}
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          <MetricCard
            title="Total Revenue"
            value="₹17.5L"
            change={12.5}
            changeLabel="vs last month"
            icon={IndianRupee}
            trend="up"
          />
          <MetricCard
            title="Net Profit"
            value="₹6.0L"
            change={8.2}
            changeLabel="vs last month"
            icon={TrendingUp}
            trend="up"
          />
          <MetricCard
            title="Outstanding Receivables"
            value="₹4.2L"
            change={-5.3}
            changeLabel="vs last month"
            icon={CreditCard}
            trend="down"
          />
          <MetricCard
            title="Cash Balance"
            value="₹8.5L"
            change={3.1}
            changeLabel="vs last month"
            icon={Wallet}
            trend="up"
          />
        </div>

        {/* Main Content Grid */}
        <div className="grid gap-6 lg:grid-cols-3">
          {/* Health Score */}
          <Card className="card-elevated">
            <CardHeader>
              <CardTitle className="text-lg">Financial Health Score</CardTitle>
            </CardHeader>
            <CardContent className="flex items-center justify-center pb-6">
              <HealthScoreGauge score={72} />
            </CardContent>
          </Card>

          {/* Revenue Chart */}
          <Card className="card-elevated lg:col-span-2">
            <CardHeader>
              <CardTitle className="text-lg">Revenue vs Expenses</CardTitle>
            </CardHeader>
            <CardContent>
              <RevenueChart data={revenueData} />
            </CardContent>
          </Card>
        </div>

        {/* Second Row */}
        <div className="grid gap-6 lg:grid-cols-2">
          {/* Expense Breakdown */}
          <Card className="card-elevated">
            <CardHeader>
              <CardTitle className="text-lg">Expense Breakdown</CardTitle>
            </CardHeader>
            <CardContent>
              <ExpenseBreakdown data={expenseData} />
            </CardContent>
          </Card>

          {/* Risk Indicators */}
          <Card className="card-elevated">
            <CardHeader>
              <CardTitle className="text-lg">Risk Assessment</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <RiskIndicator
                level="low"
                title="Liquidity Risk"
                description="Current ratio of 2.3 indicates strong liquidity position"
              />
              <RiskIndicator
                level="medium"
                title="Credit Risk"
                description="15% of receivables are overdue by 30+ days"
              />
              <RiskIndicator
                level="low"
                title="Debt Service"
                description="Debt-to-equity ratio within healthy range"
              />
            </CardContent>
          </Card>
        </div>

        {/* AI Insights */}
        <Card className="card-elevated">
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-lg">
              <span className="flex h-6 w-6 items-center justify-center rounded-full bg-accent/10">
                <ArrowUpRight className="h-3 w-3 text-accent" />
              </span>
              AI-Powered Insights
            </CardTitle>
          </CardHeader>
          <CardContent className="grid gap-4 md:grid-cols-2">
            <InsightCard
              type="opportunity"
              title="Revenue Growth Opportunity"
              description="Based on seasonal patterns, Q4 shows 25% higher demand. Consider increasing inventory by 15%."
              impact="+₹3.2L potential revenue"
            />
            <InsightCard
              type="saving"
              title="Cost Optimization"
              description="Operational costs are 12% above industry average. Consolidating vendors could reduce expenses."
              impact="₹80K monthly savings"
            />
            <InsightCard
              type="warning"
              title="Cash Flow Alert"
              description="Projected cash gap in 45 days based on current AR/AP cycle. Consider invoice factoring."
            />
            <InsightCard
              type="tip"
              title="Tax Planning"
              description="GST input credit of ₹2.1L available for claim. Ensure timely filing to avoid lapses."
            />
          </CardContent>
        </Card>

        {/* Quick Stats */}
        <div className="grid gap-4 md:grid-cols-3">
          <Card className="card-elevated border-l-4 border-l-success p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-muted-foreground">Profit Margin</p>
                <p className="mt-1 text-2xl font-bold">34.3%</p>
              </div>
              <div className="flex h-10 w-10 items-center justify-center rounded-full bg-success/10">
                <ArrowUpRight className="h-5 w-5 text-success" />
              </div>
            </div>
            <p className="mt-2 text-xs text-muted-foreground">Industry avg: 28%</p>
          </Card>

          <Card className="card-elevated border-l-4 border-l-warning p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-muted-foreground">Working Capital Days</p>
                <p className="mt-1 text-2xl font-bold">45 days</p>
              </div>
              <div className="flex h-10 w-10 items-center justify-center rounded-full bg-warning/10">
                <ArrowDownRight className="h-5 w-5 text-warning" />
              </div>
            </div>
            <p className="mt-2 text-xs text-muted-foreground">Target: 35 days</p>
          </Card>

          <Card className="card-elevated border-l-4 border-l-accent p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-muted-foreground">Debt-to-Equity</p>
                <p className="mt-1 text-2xl font-bold">0.8x</p>
              </div>
              <div className="flex h-10 w-10 items-center justify-center rounded-full bg-accent/10">
                <TrendingUp className="h-5 w-5 text-accent" />
              </div>
            </div>
            <p className="mt-2 text-xs text-muted-foreground">Healthy range: &lt;1.5x</p>
          </Card>
        </div>
      </div>
    </DashboardLayout>
  );
}
