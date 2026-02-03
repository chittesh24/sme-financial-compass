import * as React from "react";
import { cn } from "@/lib/utils";

interface StatCardProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: "default" | "success" | "warning" | "danger";
}

const StatCard = React.forwardRef<HTMLDivElement, StatCardProps>(
  ({ className, variant = "default", ...props }, ref) => {
    return (
      <div
        ref={ref}
        className={cn(
          "card-elevated p-6",
          variant === "success" && "border-l-4 border-l-success",
          variant === "warning" && "border-l-4 border-l-warning",
          variant === "danger" && "border-l-4 border-l-danger",
          className
        )}
        {...props}
      />
    );
  }
);
StatCard.displayName = "StatCard";

const StatCardHeader = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn("flex items-center justify-between", className)}
    {...props}
  />
));
StatCardHeader.displayName = "StatCardHeader";

const StatCardTitle = React.forwardRef<
  HTMLParagraphElement,
  React.HTMLAttributes<HTMLHeadingElement>
>(({ className, ...props }, ref) => (
  <h3
    ref={ref}
    className={cn("text-sm font-medium text-muted-foreground", className)}
    {...props}
  />
));
StatCardTitle.displayName = "StatCardTitle";

const StatCardValue = React.forwardRef<
  HTMLParagraphElement,
  React.HTMLAttributes<HTMLParagraphElement>
>(({ className, ...props }, ref) => (
  <p
    ref={ref}
    className={cn("mt-2 text-3xl font-bold tracking-tight", className)}
    {...props}
  />
));
StatCardValue.displayName = "StatCardValue";

const StatCardDescription = React.forwardRef<
  HTMLParagraphElement,
  React.HTMLAttributes<HTMLParagraphElement>
>(({ className, ...props }, ref) => (
  <p
    ref={ref}
    className={cn("mt-1 text-sm text-muted-foreground", className)}
    {...props}
  />
));
StatCardDescription.displayName = "StatCardDescription";

export {
  StatCard,
  StatCardHeader,
  StatCardTitle,
  StatCardValue,
  StatCardDescription,
};
