import { DashboardLayout } from "@/components/layout/DashboardLayout";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { RevenueChart } from "@/components/dashboard/RevenueChart";
import { ExpenseBreakdown } from "@/components/dashboard/ExpenseBreakdown";
import { RiskIndicator } from "@/components/dashboard/RiskIndicator";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  LineChart,
  Line,
} from "recharts";
import {
  TrendingUp,
  TrendingDown,
  DollarSign,
  CreditCard,
  Wallet,
  PieChart,
  BarChart3,
  Activity,
} from "lucide-react";

const monthlyData = [
  { month: "Jan", revenue: 1200000, expenses: 900000, profit: 300000 },
  { month: "Feb", revenue: 1350000, expenses: 950000, profit: 400000 },
  { month: "Mar", revenue: 1100000, expenses: 880000, profit: 220000 },
  { month: "Apr", revenue: 1450000, expenses: 1020000, profit: 430000 },
  { month: "May", revenue: 1600000, expenses: 1100000, profit: 500000 },
  { month: "Jun", revenue: 1750000, expenses: 1150000, profit: 600000 },
];

const cashFlowData = [
  { month: "Jan", inflow: 1150000, outflow: 950000 },
  { month: "Feb", inflow: 1400000, outflow: 1000000 },
  { month: "Mar", inflow: 1050000, outflow: 920000 },
  { month: "Apr", inflow: 1500000, outflow: 1080000 },
  { month: "May", inflow: 1650000, outflow: 1150000 },
  { month: "Jun", inflow: 1800000, outflow: 1200000 },
];

const expenseData = [
  { name: "Salaries", value: 450000 },
  { name: "Operations", value: 280000 },
  { name: "Marketing", value: 150000 },
  { name: "Inventory", value: 180000 },
  { name: "Others", value: 90000 },
];

const ratios = [
  { name: "Current Ratio", value: 2.3, benchmark: 1.5, status: "good" },
  { name: "Quick Ratio", value: 1.8, benchmark: 1.0, status: "good" },
  { name: "Debt-to-Equity", value: 0.8, benchmark: 1.5, status: "good" },
  { name: "Gross Margin", value: 42, benchmark: 35, status: "good" },
  { name: "Net Margin", value: 34.3, benchmark: 28, status: "good" },
  { name: "ROE", value: 18.5, benchmark: 15, status: "good" },
];

export default function Analysis() {
  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Header */}
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Financial Analysis</h1>
          <p className="text-muted-foreground">
            Comprehensive analysis of your business financial performance
          </p>
        </div>

        {/* Tabs */}
        <Tabs defaultValue="overview" className="space-y-6">
          <TabsList className="grid w-full grid-cols-4 lg:w-auto lg:grid-cols-4">
            <TabsTrigger value="overview" className="gap-2">
              <BarChart3 className="h-4 w-4" />
              <span className="hidden sm:inline">Overview</span>
            </TabsTrigger>
            <TabsTrigger value="profitability" className="gap-2">
              <TrendingUp className="h-4 w-4" />
              <span className="hidden sm:inline">Profitability</span>
            </TabsTrigger>
            <TabsTrigger value="cashflow" className="gap-2">
              <Activity className="h-4 w-4" />
              <span className="hidden sm:inline">Cash Flow</span>
            </TabsTrigger>
            <TabsTrigger value="ratios" className="gap-2">
              <PieChart className="h-4 w-4" />
              <span className="hidden sm:inline">Ratios</span>
            </TabsTrigger>
          </TabsList>

          {/* Overview Tab */}
          <TabsContent value="overview" className="space-y-6">
            {/* Summary Cards */}
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
              <Card className="card-elevated border-l-4 border-l-success">
                <CardContent className="p-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-muted-foreground">Total Revenue (6M)</p>
                      <p className="text-2xl font-bold">₹84.5L</p>
                    </div>
                    <TrendingUp className="h-8 w-8 text-success" />
                  </div>
                </CardContent>
              </Card>
              <Card className="card-elevated border-l-4 border-l-accent">
                <CardContent className="p-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-muted-foreground">Total Expenses (6M)</p>
                      <p className="text-2xl font-bold">₹60.0L</p>
                    </div>
                    <TrendingDown className="h-8 w-8 text-accent" />
                  </div>
                </CardContent>
              </Card>
              <Card className="card-elevated border-l-4 border-l-chart-3">
                <CardContent className="p-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-muted-foreground">Net Profit (6M)</p>
                      <p className="text-2xl font-bold">₹24.5L</p>
                    </div>
                    <DollarSign className="h-8 w-8 text-chart-3" />
                  </div>
                </CardContent>
              </Card>
              <Card className="card-elevated border-l-4 border-l-warning">
                <CardContent className="p-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-muted-foreground">Avg. Monthly Growth</p>
                      <p className="text-2xl font-bold">8.2%</p>
                    </div>
                    <TrendingUp className="h-8 w-8 text-warning" />
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* Charts */}
            <div className="grid gap-6 lg:grid-cols-2">
              <Card className="card-elevated">
                <CardHeader>
                  <CardTitle>Revenue vs Expenses</CardTitle>
                </CardHeader>
                <CardContent>
                  <RevenueChart data={monthlyData} />
                </CardContent>
              </Card>
              <Card className="card-elevated">
                <CardHeader>
                  <CardTitle>Expense Distribution</CardTitle>
                </CardHeader>
                <CardContent>
                  <ExpenseBreakdown data={expenseData} />
                </CardContent>
              </Card>
            </div>

            {/* Risk Assessment */}
            <Card className="card-elevated">
              <CardHeader>
                <CardTitle>Risk Assessment Summary</CardTitle>
              </CardHeader>
              <CardContent className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
                <RiskIndicator
                  level="low"
                  title="Liquidity Risk"
                  description="Strong current ratio indicates healthy liquidity"
                />
                <RiskIndicator
                  level="medium"
                  title="Receivables Risk"
                  description="15% of receivables overdue by 30+ days"
                />
                <RiskIndicator
                  level="low"
                  title="Debt Risk"
                  description="Conservative debt levels with strong coverage"
                />
              </CardContent>
            </Card>
          </TabsContent>

          {/* Profitability Tab */}
          <TabsContent value="profitability" className="space-y-6">
            <Card className="card-elevated">
              <CardHeader>
                <CardTitle>Monthly Profit Trend</CardTitle>
                <CardDescription>Net profit over the last 6 months</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="h-[400px]">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={monthlyData}>
                      <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
                      <XAxis dataKey="month" stroke="hsl(var(--muted-foreground))" />
                      <YAxis
                        stroke="hsl(var(--muted-foreground))"
                        tickFormatter={(value) => `₹${(value / 100000).toFixed(0)}L`}
                      />
                      <Tooltip
                        contentStyle={{
                          backgroundColor: "hsl(var(--card))",
                          border: "1px solid hsl(var(--border))",
                          borderRadius: "8px",
                        }}
                        formatter={(value: number) => [`₹${value.toLocaleString()}`, ""]}
                      />
                      <Bar
                        dataKey="profit"
                        fill="hsl(var(--success))"
                        radius={[4, 4, 0, 0]}
                        name="Net Profit"
                      />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </CardContent>
            </Card>

            <div className="grid gap-6 lg:grid-cols-3">
              <Card className="card-elevated">
                <CardContent className="p-6">
                  <div className="text-center">
                    <p className="text-sm text-muted-foreground">Gross Profit Margin</p>
                    <p className="mt-2 text-4xl font-bold text-success">42%</p>
                    <p className="mt-1 text-xs text-muted-foreground">Industry avg: 35%</p>
                  </div>
                </CardContent>
              </Card>
              <Card className="card-elevated">
                <CardContent className="p-6">
                  <div className="text-center">
                    <p className="text-sm text-muted-foreground">Operating Margin</p>
                    <p className="mt-2 text-4xl font-bold text-accent">38%</p>
                    <p className="mt-1 text-xs text-muted-foreground">Industry avg: 30%</p>
                  </div>
                </CardContent>
              </Card>
              <Card className="card-elevated">
                <CardContent className="p-6">
                  <div className="text-center">
                    <p className="text-sm text-muted-foreground">Net Profit Margin</p>
                    <p className="mt-2 text-4xl font-bold text-chart-3">34.3%</p>
                    <p className="mt-1 text-xs text-muted-foreground">Industry avg: 28%</p>
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          {/* Cash Flow Tab */}
          <TabsContent value="cashflow" className="space-y-6">
            <Card className="card-elevated">
              <CardHeader>
                <CardTitle>Cash Flow Analysis</CardTitle>
                <CardDescription>Monthly cash inflows and outflows</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="h-[400px]">
                  <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={cashFlowData}>
                      <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
                      <XAxis dataKey="month" stroke="hsl(var(--muted-foreground))" />
                      <YAxis
                        stroke="hsl(var(--muted-foreground))"
                        tickFormatter={(value) => `₹${(value / 100000).toFixed(0)}L`}
                      />
                      <Tooltip
                        contentStyle={{
                          backgroundColor: "hsl(var(--card))",
                          border: "1px solid hsl(var(--border))",
                          borderRadius: "8px",
                        }}
                        formatter={(value: number) => [`₹${value.toLocaleString()}`, ""]}
                      />
                      <Line
                        type="monotone"
                        dataKey="inflow"
                        stroke="hsl(var(--success))"
                        strokeWidth={2}
                        name="Cash Inflow"
                        dot={{ fill: "hsl(var(--success))" }}
                      />
                      <Line
                        type="monotone"
                        dataKey="outflow"
                        stroke="hsl(var(--danger))"
                        strokeWidth={2}
                        name="Cash Outflow"
                        dot={{ fill: "hsl(var(--danger))" }}
                      />
                    </LineChart>
                  </ResponsiveContainer>
                </div>
              </CardContent>
            </Card>

            <div className="grid gap-4 md:grid-cols-3">
              <Card className="card-elevated">
                <CardContent className="p-4">
                  <div className="flex items-center gap-3">
                    <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-success/10">
                      <CreditCard className="h-5 w-5 text-success" />
                    </div>
                    <div>
                      <p className="text-sm text-muted-foreground">Avg. Collection Period</p>
                      <p className="text-xl font-bold">32 days</p>
                    </div>
                  </div>
                </CardContent>
              </Card>
              <Card className="card-elevated">
                <CardContent className="p-4">
                  <div className="flex items-center gap-3">
                    <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-warning/10">
                      <Wallet className="h-5 w-5 text-warning" />
                    </div>
                    <div>
                      <p className="text-sm text-muted-foreground">Avg. Payment Period</p>
                      <p className="text-xl font-bold">28 days</p>
                    </div>
                  </div>
                </CardContent>
              </Card>
              <Card className="card-elevated">
                <CardContent className="p-4">
                  <div className="flex items-center gap-3">
                    <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-accent/10">
                      <Activity className="h-5 w-5 text-accent" />
                    </div>
                    <div>
                      <p className="text-sm text-muted-foreground">Cash Conversion Cycle</p>
                      <p className="text-xl font-bold">45 days</p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          {/* Ratios Tab */}
          <TabsContent value="ratios" className="space-y-6">
            <Card className="card-elevated">
              <CardHeader>
                <CardTitle>Financial Ratios</CardTitle>
                <CardDescription>Key performance indicators compared to industry benchmarks</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
                  {ratios.map((ratio) => (
                    <div key={ratio.name} className="rounded-lg border p-4">
                      <div className="flex items-center justify-between">
                        <p className="text-sm font-medium text-muted-foreground">{ratio.name}</p>
                        <span className="rounded-full bg-success/10 px-2 py-0.5 text-xs font-medium text-success">
                          Good
                        </span>
                      </div>
                      <p className="mt-2 text-2xl font-bold">
                        {ratio.value}{ratio.name.includes("Margin") || ratio.name.includes("ROE") ? "%" : ratio.name.includes("Ratio") || ratio.name.includes("Equity") ? "x" : ""}
                      </p>
                      <p className="mt-1 text-xs text-muted-foreground">
                        Benchmark: {ratio.benchmark}{ratio.name.includes("Margin") || ratio.name.includes("ROE") ? "%" : ratio.name.includes("Ratio") || ratio.name.includes("Equity") ? "x" : ""}
                      </p>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </DashboardLayout>
  );
}
