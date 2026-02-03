import { DashboardLayout } from "@/components/layout/DashboardLayout";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import {
  FileText,
  Download,
  Calendar,
  Eye,
  Share2,
  Sparkles,
  BarChart3,
  TrendingUp,
  DollarSign,
} from "lucide-react";

const reports = [
  {
    id: 1,
    title: "Monthly Financial Summary",
    description: "Comprehensive overview of revenue, expenses, and profitability",
    type: "summary",
    date: "Jan 2026",
    status: "ready",
  },
  {
    id: 2,
    title: "Cash Flow Statement",
    description: "Detailed analysis of cash inflows and outflows",
    type: "cashflow",
    date: "Jan 2026",
    status: "ready",
  },
  {
    id: 3,
    title: "Investor-Ready Report",
    description: "Professional report for potential investors and stakeholders",
    type: "investor",
    date: "Q4 2025",
    status: "ready",
  },
  {
    id: 4,
    title: "Tax Compliance Report",
    description: "GST summary and tax liability assessment",
    type: "tax",
    date: "Jan 2026",
    status: "processing",
  },
  {
    id: 5,
    title: "Industry Benchmarking",
    description: "Comparison with industry peers and standards",
    type: "benchmark",
    date: "Q4 2025",
    status: "ready",
  },
];

const reportTemplates = [
  {
    icon: BarChart3,
    title: "Financial Overview",
    description: "Key metrics and KPIs summary",
  },
  {
    icon: TrendingUp,
    title: "Growth Analysis",
    description: "Revenue trends and projections",
  },
  {
    icon: DollarSign,
    title: "Profitability Report",
    description: "Margin analysis and cost breakdown",
  },
  {
    icon: Sparkles,
    title: "AI Insights Report",
    description: "AI-generated recommendations",
  },
];

export default function Reports() {
  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold tracking-tight">Reports</h1>
            <p className="text-muted-foreground">
              Generate and download comprehensive financial reports
            </p>
          </div>
          <Button className="gap-2">
            <Sparkles className="h-4 w-4" />
            Generate New Report
          </Button>
        </div>

        {/* Quick Generate Templates */}
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          {reportTemplates.map((template) => (
            <Card
              key={template.title}
              className="card-elevated cursor-pointer transition-all hover:border-accent/50"
            >
              <CardContent className="p-4">
                <div className="flex items-start gap-3">
                  <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-accent/10">
                    <template.icon className="h-5 w-5 text-accent" />
                  </div>
                  <div>
                    <p className="font-medium">{template.title}</p>
                    <p className="text-sm text-muted-foreground">{template.description}</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Generated Reports */}
        <Card className="card-elevated">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <FileText className="h-5 w-5 text-accent" />
              Generated Reports
            </CardTitle>
            <CardDescription>
              View and download your previously generated reports
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {reports.map((report) => (
                <div
                  key={report.id}
                  className="flex items-center justify-between rounded-lg border p-4 transition-colors hover:bg-muted/50"
                >
                  <div className="flex items-start gap-4">
                    <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-lg bg-muted">
                      <FileText className="h-6 w-6 text-muted-foreground" />
                    </div>
                    <div>
                      <div className="flex items-center gap-2">
                        <p className="font-medium">{report.title}</p>
                        <Badge
                          variant={report.status === "ready" ? "default" : "secondary"}
                          className={
                            report.status === "ready"
                              ? "bg-success/10 text-success hover:bg-success/20"
                              : ""
                          }
                        >
                          {report.status === "ready" ? "Ready" : "Processing"}
                        </Badge>
                      </div>
                      <p className="text-sm text-muted-foreground">{report.description}</p>
                      <div className="mt-1 flex items-center gap-1 text-xs text-muted-foreground">
                        <Calendar className="h-3 w-3" />
                        {report.date}
                      </div>
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    <Button variant="ghost" size="icon" disabled={report.status !== "ready"}>
                      <Eye className="h-4 w-4" />
                    </Button>
                    <Button variant="ghost" size="icon" disabled={report.status !== "ready"}>
                      <Share2 className="h-4 w-4" />
                    </Button>
                    <Button variant="outline" size="sm" className="gap-2" disabled={report.status !== "ready"}>
                      <Download className="h-4 w-4" />
                      Download
                    </Button>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Report Insights */}
        <Card className="card-elevated">
          <CardHeader>
            <CardTitle>Report Configuration</CardTitle>
            <CardDescription>
              Customize the content and format of your reports
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid gap-4 md:grid-cols-2">
              <div className="rounded-lg border p-4">
                <p className="font-medium">Include Sections</p>
                <div className="mt-3 space-y-2">
                  {[
                    "Executive Summary",
                    "Revenue Analysis",
                    "Expense Breakdown",
                    "Cash Flow Statement",
                    "AI Insights",
                    "Industry Comparison",
                  ].map((section) => (
                    <label key={section} className="flex items-center gap-2 text-sm">
                      <input type="checkbox" defaultChecked className="rounded" />
                      {section}
                    </label>
                  ))}
                </div>
              </div>
              <div className="rounded-lg border p-4">
                <p className="font-medium">Export Options</p>
                <div className="mt-3 space-y-2">
                  <Button variant="outline" className="w-full justify-start gap-2">
                    <FileText className="h-4 w-4" />
                    Export as PDF
                  </Button>
                  <Button variant="outline" className="w-full justify-start gap-2">
                    <FileText className="h-4 w-4" />
                    Export as Excel
                  </Button>
                  <Button variant="outline" className="w-full justify-start gap-2">
                    <Share2 className="h-4 w-4" />
                    Share via Link
                  </Button>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </DashboardLayout>
  );
}
