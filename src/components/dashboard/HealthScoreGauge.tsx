import { cn } from "@/lib/utils";

interface HealthScoreGaugeProps {
  score: number;
  maxScore?: number;
  className?: string;
}

export function HealthScoreGauge({
  score,
  maxScore = 100,
  className,
}: HealthScoreGaugeProps) {
  const percentage = (score / maxScore) * 100;
  const circumference = 2 * Math.PI * 45;
  const strokeDashoffset = circumference - (percentage / 100) * circumference;

  const getScoreColor = () => {
    if (percentage >= 80) return "hsl(var(--success))";
    if (percentage >= 60) return "hsl(var(--chart-1))";
    if (percentage >= 40) return "hsl(var(--warning))";
    return "hsl(var(--danger))";
  };

  const getScoreLabel = () => {
    if (percentage >= 80) return "Excellent";
    if (percentage >= 60) return "Good";
    if (percentage >= 40) return "Fair";
    return "Needs Improvement";
  };

  return (
    <div className={cn("flex flex-col items-center", className)}>
      <div className="relative h-48 w-48">
        <svg className="h-full w-full -rotate-90 transform" viewBox="0 0 100 100">
          {/* Background circle */}
          <circle
            cx="50"
            cy="50"
            r="45"
            fill="none"
            stroke="hsl(var(--muted))"
            strokeWidth="8"
          />
          {/* Progress circle */}
          <circle
            cx="50"
            cy="50"
            r="45"
            fill="none"
            stroke={getScoreColor()}
            strokeWidth="8"
            strokeLinecap="round"
            strokeDasharray={circumference}
            strokeDashoffset={strokeDashoffset}
            className="transition-all duration-1000 ease-out"
            style={{
              filter: `drop-shadow(0 0 8px ${getScoreColor()})`,
            }}
          />
        </svg>
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <span className="text-4xl font-bold" style={{ color: getScoreColor() }}>
            {score}
          </span>
          <span className="text-sm text-muted-foreground">out of {maxScore}</span>
        </div>
      </div>
      <div className="mt-4 text-center">
        <p className="text-lg font-semibold" style={{ color: getScoreColor() }}>
          {getScoreLabel()}
        </p>
        <p className="text-sm text-muted-foreground">Financial Health Score</p>
      </div>
    </div>
  );
}
