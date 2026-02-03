import { cn } from "@/lib/utils";
import { AlertTriangle, CheckCircle2, XCircle, AlertCircle } from "lucide-react";

export type RiskLevel = "low" | "medium" | "high" | "critical";

interface RiskIndicatorProps {
  level: RiskLevel;
  title: string;
  description: string;
  className?: string;
}

const riskConfig = {
  low: {
    icon: CheckCircle2,
    label: "Low Risk",
    bgColor: "bg-success/10",
    textColor: "text-success",
    borderColor: "border-success/20",
  },
  medium: {
    icon: AlertCircle,
    label: "Medium Risk",
    bgColor: "bg-warning/10",
    textColor: "text-warning",
    borderColor: "border-warning/20",
  },
  high: {
    icon: AlertTriangle,
    label: "High Risk",
    bgColor: "bg-danger/10",
    textColor: "text-danger",
    borderColor: "border-danger/20",
  },
  critical: {
    icon: XCircle,
    label: "Critical Risk",
    bgColor: "bg-destructive/10",
    textColor: "text-destructive",
    borderColor: "border-destructive/20",
  },
};

export function RiskIndicator({
  level,
  title,
  description,
  className,
}: RiskIndicatorProps) {
  const config = riskConfig[level];
  const Icon = config.icon;

  return (
    <div
      className={cn(
        "flex items-start gap-3 rounded-lg border p-4",
        config.bgColor,
        config.borderColor,
        className
      )}
    >
      <div className={cn("mt-0.5", config.textColor)}>
        <Icon className="h-5 w-5" />
      </div>
      <div className="flex-1 space-y-1">
        <div className="flex items-center justify-between">
          <p className="font-medium">{title}</p>
          <span
            className={cn(
              "rounded-full px-2 py-0.5 text-xs font-medium",
              config.bgColor,
              config.textColor
            )}
          >
            {config.label}
          </span>
        </div>
        <p className="text-sm text-muted-foreground">{description}</p>
      </div>
    </div>
  );
}
