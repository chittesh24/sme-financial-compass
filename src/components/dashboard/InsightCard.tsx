import { cn } from "@/lib/utils";
import { LucideIcon, Lightbulb, TrendingUp, AlertTriangle, DollarSign } from "lucide-react";

type InsightType = "tip" | "opportunity" | "warning" | "saving";

interface InsightCardProps {
  type: InsightType;
  title: string;
  description: string;
  impact?: string;
  className?: string;
}

const insightConfig: Record<InsightType, { icon: LucideIcon; bgColor: string; iconColor: string }> = {
  tip: {
    icon: Lightbulb,
    bgColor: "bg-accent/10",
    iconColor: "text-accent",
  },
  opportunity: {
    icon: TrendingUp,
    bgColor: "bg-success/10",
    iconColor: "text-success",
  },
  warning: {
    icon: AlertTriangle,
    bgColor: "bg-warning/10",
    iconColor: "text-warning",
  },
  saving: {
    icon: DollarSign,
    bgColor: "bg-chart-3/10",
    iconColor: "text-chart-3",
  },
};

export function InsightCard({
  type,
  title,
  description,
  impact,
  className,
}: InsightCardProps) {
  const config = insightConfig[type];
  const Icon = config.icon;

  return (
    <div
      className={cn(
        "card-elevated flex gap-4 p-4",
        className
      )}
    >
      <div
        className={cn(
          "flex h-10 w-10 shrink-0 items-center justify-center rounded-lg",
          config.bgColor
        )}
      >
        <Icon className={cn("h-5 w-5", config.iconColor)} />
      </div>
      <div className="flex-1 space-y-1">
        <p className="font-medium">{title}</p>
        <p className="text-sm text-muted-foreground">{description}</p>
        {impact && (
          <p className={cn("text-sm font-medium", config.iconColor)}>
            Potential impact: {impact}
          </p>
        )}
      </div>
    </div>
  );
}
