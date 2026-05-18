import { Navigate, Outlet } from "react-router-dom";
import { useAuth } from "../../hooks/useAuth";
import type { UserRole } from "../../types";

interface Props {
  requiredRole?: UserRole | UserRole[];
}

function roleHome(role?: UserRole): string {
  if (role === "admin") return "/admin";
  if (role === "agent") return "/agent";
  return "/home";
}

export default function ProtectedRoute({ requiredRole }: Props) {
  const { isAuthenticated, isLoading, user } = useAuth();

  if (isLoading) {
    return (
      <div className="flex h-screen items-center justify-center">
        <span className="text-gray-500">Loading...</span>
      </div>
    );
  }

  if (!isAuthenticated) return <Navigate to="/login" replace />;

  if (requiredRole) {
    const allowed = Array.isArray(requiredRole) ? requiredRole : [requiredRole];
    if (!user?.role || !allowed.includes(user.role)) {
      return <Navigate to={roleHome(user?.role)} replace />;
    }
  }

  return <Outlet />;
}
