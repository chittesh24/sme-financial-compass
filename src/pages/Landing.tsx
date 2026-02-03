import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { useNavigate } from "react-router-dom";
import {
  TrendingUp,
  Shield,
  BarChart3,
  Sparkles,
  FileText,
  Globe,
  ArrowRight,
  CheckCircle2,
} from "lucide-react";

const features = [
  {
    icon: BarChart3,
    title: "Financial Analysis",
    description: "Comprehensive analysis of revenue, expenses, cash flow, and profitability metrics.",
  },
  {
    icon: Sparkles,
    title: "AI-Powered Insights",
    description: "Get actionable recommendations and forecasts powered by advanced AI models.",
  },
  {
    icon: Shield,
    title: "Risk Assessment",
    description: "Identify financial risks early with creditworthiness and liquidity analysis.",
  },
  {
    icon: FileText,
    title: "Smart Reports",
    description: "Generate investor-ready reports with beautiful visualizations.",
  },
  {
    icon: TrendingUp,
    title: "Forecasting",
    description: "Predict revenue trends, cash flow, and growth scenarios.",
  },
  {
    icon: Globe,
    title: "Multilingual",
    description: "Support for English and Hindi for regional business owners.",
  },
];

const benefits = [
  "Upload CSV, XLSX, or PDF financial statements",
  "Industry-specific benchmarking",
  "Working capital optimization",
  "Tax compliance checking",
  "Financial product recommendations",
  "Secure data encryption",
];

export default function Landing() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-background">
      {/* Navigation */}
      <nav className="border-b bg-card/50 backdrop-blur-sm">
        <div className="container mx-auto flex h-16 items-center justify-between px-4">
          <div className="flex items-center gap-2">
            <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-primary">
              <TrendingUp className="h-5 w-5 text-primary-foreground" />
            </div>
            <span className="text-xl font-bold">FinHealth</span>
          </div>
          <div className="flex items-center gap-4">
            <Button variant="ghost" onClick={() => navigate("/auth")}>
              Sign In
            </Button>
            <Button onClick={() => navigate("/auth?mode=signup")}>
              Get Started
            </Button>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="relative overflow-hidden">
        <div
          className="absolute inset-0 -z-10"
          style={{
            background: "var(--gradient-hero)",
          }}
        />
        <div className="container mx-auto px-4 py-24 text-center">
          <div className="mx-auto max-w-3xl">
            <div className="mb-6 inline-flex items-center gap-2 rounded-full border border-white/10 bg-white/5 px-4 py-1.5 text-sm text-white/80 backdrop-blur-sm">
              <Sparkles className="h-4 w-4" />
              AI-Powered Financial Intelligence
            </div>
            <h1 className="mb-6 text-4xl font-bold tracking-tight text-white sm:text-5xl lg:text-6xl">
              Financial Health Assessment for{" "}
              <span className="bg-gradient-to-r from-accent to-success bg-clip-text text-transparent">
                SMEs
              </span>
            </h1>
            <p className="mb-8 text-lg text-white/70 sm:text-xl">
              Analyze your financial statements, identify risks, and get AI-powered
              recommendations to grow your business. Built for small and medium
              enterprises in India.
            </p>
            <div className="flex flex-col items-center justify-center gap-4 sm:flex-row">
              <Button
                size="lg"
                className="gap-2 bg-accent text-accent-foreground hover:bg-accent/90"
                onClick={() => navigate("/auth?mode=signup")}
              >
                Start Free Analysis
                <ArrowRight className="h-4 w-4" />
              </Button>
              <Button
                size="lg"
                variant="outline"
                className="border-white/20 bg-white/5 text-white hover:bg-white/10"
                onClick={() => navigate("/dashboard")}
              >
                View Demo
              </Button>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-24">
        <div className="container mx-auto px-4">
          <div className="mb-16 text-center">
            <h2 className="mb-4 text-3xl font-bold tracking-tight sm:text-4xl">
              Everything you need for financial clarity
            </h2>
            <p className="mx-auto max-w-2xl text-muted-foreground">
              Comprehensive tools designed specifically for Indian SMEs to understand,
              analyze, and improve their financial health.
            </p>
          </div>
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            {features.map((feature) => (
              <Card key={feature.title} className="card-elevated">
                <CardContent className="p-6">
                  <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-lg bg-accent/10">
                    <feature.icon className="h-6 w-6 text-accent" />
                  </div>
                  <h3 className="mb-2 text-lg font-semibold">{feature.title}</h3>
                  <p className="text-muted-foreground">{feature.description}</p>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Benefits Section */}
      <section className="border-y bg-muted/30 py-24">
        <div className="container mx-auto px-4">
          <div className="grid items-center gap-12 lg:grid-cols-2">
            <div>
              <h2 className="mb-6 text-3xl font-bold tracking-tight sm:text-4xl">
                Built for Indian businesses
              </h2>
              <p className="mb-8 text-muted-foreground">
                From manufacturing to services, retail to e-commerce — our platform
                understands the unique challenges of Indian SMEs and provides
                industry-specific insights.
              </p>
              <ul className="grid gap-3 sm:grid-cols-2">
                {benefits.map((benefit) => (
                  <li key={benefit} className="flex items-center gap-2">
                    <CheckCircle2 className="h-5 w-5 shrink-0 text-success" />
                    <span className="text-sm">{benefit}</span>
                  </li>
                ))}
              </ul>
            </div>
            <div className="relative">
              <div className="aspect-video overflow-hidden rounded-xl border bg-card shadow-xl">
                <div className="flex h-full flex-col items-center justify-center p-8">
                  <div className="mb-4 flex h-16 w-16 items-center justify-center rounded-full bg-accent/10">
                    <BarChart3 className="h-8 w-8 text-accent" />
                  </div>
                  <p className="text-center text-lg font-medium">
                    Upload your financial data and get insights in minutes
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-24">
        <div className="container mx-auto px-4">
          <div className="mx-auto max-w-3xl text-center">
            <h2 className="mb-6 text-3xl font-bold tracking-tight sm:text-4xl">
              Ready to improve your financial health?
            </h2>
            <p className="mb-8 text-muted-foreground">
              Join thousands of SMEs using FinHealth to make better financial decisions.
              Start your free analysis today.
            </p>
            <Button
              size="lg"
              className="gap-2"
              onClick={() => navigate("/auth?mode=signup")}
            >
              Get Started Free
              <ArrowRight className="h-4 w-4" />
            </Button>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t py-8">
        <div className="container mx-auto flex flex-col items-center justify-between gap-4 px-4 text-sm text-muted-foreground sm:flex-row">
          <div className="flex items-center gap-2">
            <TrendingUp className="h-5 w-5" />
            <span>FinHealth © 2026</span>
          </div>
          <div className="flex gap-6">
            <a href="#" className="hover:text-foreground">Privacy Policy</a>
            <a href="#" className="hover:text-foreground">Terms of Service</a>
            <a href="#" className="hover:text-foreground">Contact</a>
          </div>
        </div>
      </footer>
    </div>
  );
}
