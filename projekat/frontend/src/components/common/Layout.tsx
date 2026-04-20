import { Outlet, Link, useNavigate } from "react-router-dom";
import { useAuth } from "../../hooks/useAuth";

export default function Layout() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  function handleLogout() {
    logout();
    navigate("/login");
  }

  return (
    <div className="min-h-screen flex flex-col">
      {/* Navbar */}
      <nav className="bg-primary-700 text-white px-6 py-3 flex items-center justify-between shadow">
        <div className="flex items-center gap-6">
          <Link to="/" className="font-semibold text-lg tracking-tight">
            Call Centar Chatbot
          </Link>
          {user?.role === "admin" && (
            <Link to="/admin" className="text-sm hover:underline opacity-90">
              Admin panel
            </Link>
          )}
        </div>
        <div className="flex items-center gap-4 text-sm">
          <span className="opacity-75">{user?.email}</span>
          <span className="bg-white/20 rounded px-2 py-0.5 text-xs uppercase tracking-wide">
            {user?.role}
          </span>
          <button
            onClick={handleLogout}
            className="hover:underline opacity-90"
          >
            Odjava
          </button>
        </div>
      </nav>

      {/* Page content */}
      <main className="flex-1 flex flex-col">
        <Outlet />
      </main>
    </div>
  );
}
