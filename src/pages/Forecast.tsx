import { DashboardLayout } from "@/components/layout/DashboardLayout";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Slider } from "@/components/ui/slider";
import { Label } from "@/components/ui/label";
import { useState } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
  Area,
  AreaChart,
} from "recharts";
import {
  TrendingUp,
  Calendar,
  Target,
  Activity,
  ArrowUpRight,
  ArrowDownRight,
  RefreshCw,
} from "lucide-react";

const historicalData = [
  { month: "Jan", actual: 1200000 },
  { month: "Feb", actual: 1350000 },
  { month: "Mar", actual: 1100000 },
  { month: "Apr", actual: 1450000 },
  { month: "May", actual: 1600000 },
  { month: "Jun", actual: 1750000 },
];

const forecastData = [
  { month: "Jul", forecast: 1850000, low: 1700000, high: 2000000 },
  { month: "Aug", forecast: 1920000, low: 1750000, high: 2100000 },
  { month: "Sep", forecast: 2050000, low: 1850000, high: 2250000 },
  { month: "Oct", forecast: 2180000, low: 1950000, high: 2400000 },
  { month: "Nov", forecast: 2350000, low: 2100000, high: 2600000 },
  { month: "Dec", forecast: 2500000, low: 2200000, high: 2800000 },
];

const combinedData = [
  ...historicalData.map((d) => ({ ...d, type: "historical" })),
  { month: "Jun", actual: 1750000, forecast: 1750000, type: "transition" },
  ...forecastData.map((d) => ({ ...d, type: "forecast" })),
];

export default function Forecast() {
  const [forecastPeriod, setForecastPeriod] = useState("6");
  const [growthRate, setGrowthRate] = useState([8]);

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold tracking-tight">Financial Forecasting</h1>
            <p className="text-muted-foreground">
              AI-powered predictions for revenue, expenses, and cash flow
            </p>
          </div>
          <Button className="gap-2">
            <RefreshCw className="h-4 w-4" />
            Regenerate Forecast
          </Button>
        </div>

        {/* Forecast Parameters */}
        <Card className="card-elevated">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Target className="h-5 w-5 text-accent" />
              Forecast Parameters
            </CardTitle>
            <CardDescription>
              Adjust parameters to customize your financial projections
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid gap-6 md:grid-cols-3">
              <div className="space-y-2">
                <Label>Forecast Period</Label>
                <Select value={forecastPeriod} onValueChange={setForecastPeriod}>
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="3">3 Months</SelectItem>
                    <SelectItem value="6">6 Months</SelectItem>
                    <SelectItem value="12">12 Months</SelectItem>
                    <SelectItem value="24">24 Months</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <Label>Expected Growth Rate</Label>
                  <span className="text-sm font-medium">{growthRate[0]}%</span>
                </div>
                <Slider
                  value={growthRate}
                  onValueChange={setGrowthRate}
                  min={0}
                  max={25}
                  step={1}
                />
              </div>
              <div className="space-y-2">
                <Label>Scenario</Label>
                <Select defaultValue="moderate">
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="conservative">Conservative</SelectItem>
                    <SelectItem value="moderate">Moderate</SelectItem>
                    <SelectItem value="aggressive">Aggressive</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Revenue Forecast Chart */}
        <Card className="card-elevated">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <TrendingUp className="h-5 w-5 text-success" />
              Revenue Forecast
            </CardTitle>
            <CardDescription>
              Historical data with AI-generated projections and confidence intervals
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="h-[400px]">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={combinedData}>
                  <defs>
                    <linearGradient id="forecastGradient" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="hsl(var(--accent))" stopOpacity={0.3} />
                      <stop offset="95%" stopColor="hsl(var(--accent))" stopOpacity={0} />
                    </linearGradient>
                  </defs>
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
                  <Legend />
                  <Area
                    type="monotone"
                    dataKey="high"
                    stroke="none"
                    fill="hsl(var(--muted))"
                    fillOpacity={0.3}
                    name="Upper Bound"
                  />
                  <Area
                    type="monotone"
                    dataKey="low"
                    stroke="none"
                    fill="hsl(var(--background))"
                    name="Lower Bound"
                  />
                  <Line
                    type="monotone"
                    dataKey="actual"
                    stroke="hsl(var(--chart-2))"
                    strokeWidth={2}
                    dot={{ fill: "hsl(var(--chart-2))" }}
                    name="Actual"
                  />
                  <Line
                    type="monotone"
                    dataKey="forecast"
                    stroke="hsl(var(--accent))"
                    strokeWidth={2}
                    strokeDasharray="5 5"
                    dot={{ fill: "hsl(var(--accent))" }}
                    name="Forecast"
                  />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>

        {/* Forecast Summary Cards */}
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          <Card className="card-elevated">
            <CardContent className="p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-muted-foreground">Projected Q3 Revenue</p>
                  <p className="mt-1 text-2xl font-bold">₹58.2L</p>
                </div>
                <div className="flex h-10 w-10 items-center justify-center rounded-full bg-success/10">
                  <ArrowUpRight className="h-5 w-5 text-success" />
                </div>
              </div>
              <p className="mt-2 text-xs text-success">+15% vs Q2</p>
            </CardContent>
          </Card>

          <Card className="card-elevated">
            <CardContent className="p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-muted-foreground">Projected Expenses</p>
                  <p className="mt-1 text-2xl font-bold">₹38.5L</p>
                </div>
                <div className="flex h-10 w-10 items-center justify-center rounded-full bg-warning/10">
                  <ArrowDownRight className="h-5 w-5 text-warning" />
                </div>
              </div>
              <p className="mt-2 text-xs text-warning">+12% vs Q2</p>
            </CardContent>
          </Card>

          <Card className="card-elevated">
            <CardContent className="p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-muted-foreground">Projected Net Profit</p>
                  <p className="mt-1 text-2xl font-bold">₹19.7L</p>
                </div>
                <div className="flex h-10 w-10 items-center justify-center rounded-full bg-accent/10">
                  <TrendingUp className="h-5 w-5 text-accent" />
                </div>
              </div>
              <p className="mt-2 text-xs text-success">+22% vs Q2</p>
            </CardContent>
          </Card>

          <Card className="card-elevated">
            <CardContent className="p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-muted-foreground">Confidence Level</p>
                  <p className="mt-1 text-2xl font-bold">85%</p>
                </div>
                <div className="flex h-10 w-10 items-center justify-center rounded-full bg-chart-3/10">
                  <Activity className="h-5 w-5 text-chart-3" />
                </div>
              </div>
              <p className="mt-2 text-xs text-muted-foreground">Based on historical data</p>
            </CardContent>
          </Card>
        </div>

        {/* Scenario Analysis */}
        <Card className="card-elevated">
          <CardHeader>
            <CardTitle>Scenario Analysis</CardTitle>
            <CardDescription>
              Compare different growth scenarios for your business
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid gap-4 md:grid-cols-3">
              <div className="rounded-lg border border-warning/30 bg-warning/5 p-4">
                <p className="font-medium text-warning">Conservative</p>
                <p className="mt-2 text-2xl font-bold">₹48.5L</p>
                <p className="text-sm text-muted-foreground">Q3 Revenue</p>
                <p className="mt-2 text-xs text-warning">Growth: 5%</p>
              </div>
              <div className="rounded-lg border border-accent/30 bg-accent/5 p-4">
                <p className="font-medium text-accent">Moderate</p>
                <p className="mt-2 text-2xl font-bold">₹58.2L</p>
                <p className="text-sm text-muted-foreground">Q3 Revenue</p>
                <p className="mt-2 text-xs text-accent">Growth: 12%</p>
              </div>
              <div className="rounded-lg border border-success/30 bg-success/5 p-4">
                <p className="font-medium text-success">Aggressive</p>
                <p className="mt-2 text-2xl font-bold">₹72.8L</p>
                <p className="text-sm text-muted-foreground">Q3 Revenue</p>
                <p className="mt-2 text-xs text-success">Growth: 20%</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </DashboardLayout>
  );
}
