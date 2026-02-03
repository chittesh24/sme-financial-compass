import { useState } from "react";
import { DashboardLayout } from "@/components/layout/DashboardLayout";
import { FileUpload } from "@/components/upload/FileUpload";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { useNavigate } from "react-router-dom";
import {
  FileSpreadsheet,
  FileText,
  AlertCircle,
  ArrowRight,
  Building2,
  Calendar,
  Loader2,
} from "lucide-react";
import { useToast } from "@/hooks/use-toast";

const industries = [
  "Manufacturing",
  "Retail",
  "Services",
  "Agriculture",
  "Logistics",
  "E-commerce",
  "Healthcare",
  "Construction",
  "Food & Beverage",
  "Technology",
];

const fiscalYears = [
  "FY 2025-26",
  "FY 2024-25",
  "FY 2023-24",
  "FY 2022-23",
];

export default function Upload() {
  const navigate = useNavigate();
  const { toast } = useToast();
  const [files, setFiles] = useState<File[]>([]);
  const [businessName, setBusinessName] = useState("");
  const [industry, setIndustry] = useState("");
  const [fiscalYear, setFiscalYear] = useState("");
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  const handleFilesSelected = (selectedFiles: File[]) => {
    setFiles((prev) => [...prev, ...selectedFiles]);
  };

  const handleAnalyze = async () => {
    if (files.length === 0) {
      toast({
        title: "No files selected",
        description: "Please upload at least one financial document to analyze.",
        variant: "destructive",
      });
      return;
    }

    if (!businessName || !industry || !fiscalYear) {
      toast({
        title: "Missing information",
        description: "Please fill in all business details before analyzing.",
        variant: "destructive",
      });
      return;
    }

    setIsAnalyzing(true);
    
    // Simulate analysis process
    await new Promise((resolve) => setTimeout(resolve, 3000));
    
    toast({
      title: "Analysis complete",
      description: "Your financial data has been analyzed. View the results on the dashboard.",
    });
    
    setIsAnalyzing(false);
    navigate("/dashboard");
  };

  return (
    <DashboardLayout>
      <div className="mx-auto max-w-4xl space-y-6">
        {/* Header */}
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Upload Financial Data</h1>
          <p className="text-muted-foreground">
            Upload your financial statements to get AI-powered insights and recommendations.
          </p>
        </div>

        {/* Business Details */}
        <Card className="card-elevated">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Building2 className="h-5 w-5 text-accent" />
              Business Details
            </CardTitle>
            <CardDescription>
              Provide basic information about your business for industry-specific analysis.
            </CardDescription>
          </CardHeader>
          <CardContent className="grid gap-4 sm:grid-cols-3">
            <div className="space-y-2">
              <Label htmlFor="businessName">Business Name</Label>
              <Input
                id="businessName"
                placeholder="Enter business name"
                value={businessName}
                onChange={(e) => setBusinessName(e.target.value)}
              />
            </div>
            <div className="space-y-2">
              <Label>Industry</Label>
              <Select value={industry} onValueChange={setIndustry}>
                <SelectTrigger>
                  <SelectValue placeholder="Select industry" />
                </SelectTrigger>
                <SelectContent>
                  {industries.map((ind) => (
                    <SelectItem key={ind} value={ind.toLowerCase()}>
                      {ind}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
            <div className="space-y-2">
              <Label>Fiscal Year</Label>
              <Select value={fiscalYear} onValueChange={setFiscalYear}>
                <SelectTrigger>
                  <SelectValue placeholder="Select fiscal year" />
                </SelectTrigger>
                <SelectContent>
                  {fiscalYears.map((fy) => (
                    <SelectItem key={fy} value={fy}>
                      {fy}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          </CardContent>
        </Card>

        {/* File Upload */}
        <Card className="card-elevated">
          <CardHeader>
            <CardTitle>Upload Documents</CardTitle>
            <CardDescription>
              Upload your financial statements, P&L reports, balance sheets, or bank statements.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <FileUpload onFilesSelected={handleFilesSelected} />
          </CardContent>
        </Card>

        {/* Supported Formats */}
        <div className="grid gap-4 sm:grid-cols-3">
          <Card className="card-elevated">
            <CardContent className="flex items-start gap-3 p-4">
              <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-success/10">
                <FileSpreadsheet className="h-5 w-5 text-success" />
              </div>
              <div>
                <p className="font-medium">CSV / Excel</p>
                <p className="text-sm text-muted-foreground">
                  Tally exports, bank statements, transaction data
                </p>
              </div>
            </CardContent>
          </Card>
          <Card className="card-elevated">
            <CardContent className="flex items-start gap-3 p-4">
              <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-accent/10">
                <FileText className="h-5 w-5 text-accent" />
              </div>
              <div>
                <p className="font-medium">PDF Reports</p>
                <p className="text-sm text-muted-foreground">
                  Audited statements, GST returns, ITR forms
                </p>
              </div>
            </CardContent>
          </Card>
          <Card className="card-elevated">
            <CardContent className="flex items-start gap-3 p-4">
              <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-warning/10">
                <AlertCircle className="h-5 w-5 text-warning" />
              </div>
              <div>
                <p className="font-medium">Secure Upload</p>
                <p className="text-sm text-muted-foreground">
                  All data is encrypted and securely processed
                </p>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Analyze Button */}
        <div className="flex justify-end gap-4">
          <Button variant="outline" onClick={() => navigate("/dashboard")}>
            Skip for Now
          </Button>
          <Button
            onClick={handleAnalyze}
            disabled={isAnalyzing}
            className="gap-2"
          >
            {isAnalyzing ? (
              <>
                <Loader2 className="h-4 w-4 animate-spin" />
                Analyzing...
              </>
            ) : (
              <>
                Start Analysis
                <ArrowRight className="h-4 w-4" />
              </>
            )}
          </Button>
        </div>
      </div>
    </DashboardLayout>
  );
}
