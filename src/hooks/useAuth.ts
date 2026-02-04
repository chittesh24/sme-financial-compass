/**
 * Unified Authentication Hook
 * Handles both Supabase and custom JWT authentication
 */
import { useNavigate } from "react-router-dom";
import { supabase } from "@/integrations/supabase/client";
import { useToast } from "@/hooks/use-toast";

export const useAuth = () => {
  const navigate = useNavigate();
  const { toast } = useToast();

  const handleLogout = async () => {
    try {
      // Sign out from Supabase
      await supabase.auth.signOut();
      
      // Clear local storage (custom JWT tokens)
      localStorage.removeItem('access_token');
      localStorage.removeItem('user');
      
      // Show success message
      toast({
        title: "Logged out successfully",
        description: "You have been logged out of your account.",
      });
      
      // Redirect to auth page
      navigate('/auth');
    } catch (error: any) {
      console.error('Logout error:', error);
      toast({
        title: "Logout error",
        description: error.message || "Failed to logout. Please try again.",
        variant: "destructive",
      });
    }
  };

  const getCurrentUser = () => {
    const user = localStorage.getItem('user');
    return user ? JSON.parse(user) : null;
  };

  const isAuthenticated = () => {
    return !!localStorage.getItem('access_token');
  };

  return {
    handleLogout,
    getCurrentUser,
    isAuthenticated,
  };
};
