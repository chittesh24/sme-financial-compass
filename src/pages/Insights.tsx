import { useState } from "react";
import { DashboardLayout } from "@/components/layout/DashboardLayout";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { InsightCard } from "@/components/dashboard/InsightCard";
import {
  Sparkles,
  Send,
  Loader2,
  TrendingUp,
  AlertTriangle,
  Lightbulb,
  DollarSign,
  RefreshCw,
} from "lucide-react";
import { useToast } from "@/hooks/use-toast";

interface Message {
  role: "user" | "assistant";
  content: string;
}

const preGeneratedInsights = [
  {
    type: "opportunity" as const,
    title: "Revenue Growth Potential",
    description: "Based on your Q3 performance, expanding into adjacent markets could increase revenue by 15-20%. Consider partnerships with complementary businesses.",
    impact: "+₹4.5L annual revenue",
  },
  {
    type: "warning" as const,
    title: "Working Capital Gap",
    description: "Your receivables cycle has increased from 35 to 48 days. Implementing stricter credit terms could improve cash flow by ₹2L monthly.",
  },
  {
    type: "saving" as const,
    title: "Operational Efficiency",
    description: "Your utility costs are 18% above industry benchmark. Energy audit and process optimization could reduce monthly expenses.",
    impact: "₹45K monthly savings",
  },
  {
    type: "tip" as const,
    title: "Tax Optimization",
    description: "You're eligible for MSME tax benefits that could reduce your effective tax rate by 2-3%. Consult with your CA for Section 44AD benefits.",
    impact: "₹1.2L annual savings",
  },
];

export default function Insights() {
  const { toast } = useToast();
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage: Message = { role: "user", content: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);

    // Simulate AI response
    await new Promise((resolve) => setTimeout(resolve, 2000));
    
    const assistantMessage: Message = {
      role: "assistant",
      content: `Based on your query about "${input}", here's my analysis:

Your financial data shows strong revenue growth of 12.5% month-over-month. However, I notice a few areas for optimization:

1. **Cash Flow Management**: Your current ratio is 2.3, which is healthy, but working capital days could be reduced from 45 to 35 days by improving accounts receivable collection.

2. **Cost Structure**: Operating expenses represent 34% of revenue, slightly above the industry average of 28%. Consider renegotiating vendor contracts.

3. **Growth Opportunity**: Given your profit margins, you have capacity to invest in marketing, which typically yields 3-4x returns in your industry.

Would you like me to elaborate on any of these points?`,
    };
    
    setMessages((prev) => [...prev, assistantMessage]);
    setIsLoading(false);
  };

  const handleRefreshInsights = () => {
    toast({
      title: "Insights refreshed",
      description: "AI insights have been updated based on your latest data.",
    });
  };

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold tracking-tight">AI Insights</h1>
            <p className="text-muted-foreground">
              Get personalized financial insights and recommendations powered by AI.
            </p>
          </div>
          <Button variant="outline" className="gap-2" onClick={handleRefreshInsights}>
            <RefreshCw className="h-4 w-4" />
            Refresh Insights
          </Button>
        </div>

        {/* Pre-generated Insights */}
        <Card className="card-elevated">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-accent/10">
                <Sparkles className="h-4 w-4 text-accent" />
              </div>
              Key Recommendations
            </CardTitle>
            <CardDescription>
              AI-generated insights based on your financial data analysis
            </CardDescription>
          </CardHeader>
          <CardContent className="grid gap-4 md:grid-cols-2">
            {preGeneratedInsights.map((insight, index) => (
              <InsightCard key={index} {...insight} />
            ))}
          </CardContent>
        </Card>

        {/* AI Chat */}
        <Card className="card-elevated">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary/10">
                <Lightbulb className="h-4 w-4 text-primary" />
              </div>
              Ask Financial Advisor
            </CardTitle>
            <CardDescription>
              Ask questions about your financial health, get personalized advice
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {/* Chat Messages */}
              {messages.length > 0 && (
                <div className="max-h-96 space-y-4 overflow-y-auto rounded-lg border bg-muted/30 p-4">
                  {messages.map((message, index) => (
                    <div
                      key={index}
                      className={`flex ${message.role === "user" ? "justify-end" : "justify-start"}`}
                    >
                      <div
                        className={`max-w-[80%] rounded-lg px-4 py-2 ${
                          message.role === "user"
                            ? "bg-primary text-primary-foreground"
                            : "bg-card border"
                        }`}
                      >
                        <p className="whitespace-pre-wrap text-sm">{message.content}</p>
                      </div>
                    </div>
                  ))}
                  {isLoading && (
                    <div className="flex justify-start">
                      <div className="flex items-center gap-2 rounded-lg border bg-card px-4 py-2">
                        <Loader2 className="h-4 w-4 animate-spin" />
                        <span className="text-sm text-muted-foreground">Analyzing...</span>
                      </div>
                    </div>
                  )}
                </div>
              )}

              {/* Input Form */}
              <form onSubmit={handleSubmit} className="flex gap-2">
                <Textarea
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  placeholder="Ask about your financial health, cost optimization, growth strategies..."
                  className="min-h-[80px] resize-none"
                  onKeyDown={(e) => {
                    if (e.key === "Enter" && !e.shiftKey) {
                      e.preventDefault();
                      handleSubmit(e);
                    }
                  }}
                />
                <Button
                  type="submit"
                  size="icon"
                  className="h-auto w-12 shrink-0"
                  disabled={isLoading || !input.trim()}
                >
                  <Send className="h-4 w-4" />
                </Button>
              </form>

              {/* Suggested Questions */}
              <div className="flex flex-wrap gap-2">
                <span className="text-sm text-muted-foreground">Try asking:</span>
                {[
                  "How can I improve cash flow?",
                  "What are my biggest risks?",
                  "Suggest cost reduction strategies",
                ].map((question) => (
                  <Button
                    key={question}
                    variant="outline"
                    size="sm"
                    onClick={() => setInput(question)}
                  >
                    {question}
                  </Button>
                ))}
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Industry Comparison */}
        <Card className="card-elevated">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <TrendingUp className="h-5 w-5 text-accent" />
              Industry Benchmarking
            </CardTitle>
            <CardDescription>
              See how your metrics compare to industry averages
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {[
                { metric: "Profit Margin", yours: 34.3, industry: 28.0, better: true },
                { metric: "Current Ratio", yours: 2.3, industry: 1.8, better: true },
                { metric: "Working Capital Days", yours: 45, industry: 35, better: false },
                { metric: "Debt-to-Equity", yours: 0.8, industry: 1.2, better: true },
              ].map((item) => (
                <div key={item.metric} className="flex items-center justify-between rounded-lg border p-4">
                  <div>
                    <p className="font-medium">{item.metric}</p>
                    <p className="text-sm text-muted-foreground">
                      Industry avg: {item.industry}{item.metric.includes("Ratio") || item.metric.includes("Equity") ? "x" : item.metric.includes("Days") ? " days" : "%"}
                    </p>
                  </div>
                  <div className="text-right">
                    <p className={`text-lg font-bold ${item.better ? "text-success" : "text-warning"}`}>
                      {item.yours}{item.metric.includes("Ratio") || item.metric.includes("Equity") ? "x" : item.metric.includes("Days") ? " days" : "%"}
                    </p>
                    <p className={`text-xs ${item.better ? "text-success" : "text-warning"}`}>
                      {item.better ? "Above average" : "Below average"}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </DashboardLayout>
  );
}
