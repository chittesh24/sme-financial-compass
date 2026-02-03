import { ReactNode } from "react";
import { Sidebar } from "./Sidebar";
import { cn } from "@/lib/utils";

interface DashboardLayoutProps {
  children: ReactNode;
  onLogout?: () => void;
}

export function DashboardLayout({ children, onLogout }: DashboardLayoutProps) {
  return (
    <div className="min-h-screen bg-background">
      <Sidebar onLogout={onLogout} />
      <main className={cn("ml-64 min-h-screen transition-all duration-300")}>
        <div className="container mx-auto p-6">{children}</div>
      </main>
    </div>
  );
}
