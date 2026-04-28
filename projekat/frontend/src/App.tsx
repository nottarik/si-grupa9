import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import LoginPage from "./pages/LoginPage";
import ChatPage from "./pages/ChatPage";
import AdminPage from "./pages/AdminPage";
import ProtectedRoute from "./components/common/ProtectedRoute";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<LoginPage />} />

        {/* Protected routes – any authenticated user */}
        <Route element={<ProtectedRoute />}>
          <Route path="/" element={<ChatPage />} />
        </Route>

        {/* Admin panel – admin role required */}
        <Route element={<ProtectedRoute requiredRole="admin" />}>
          <Route path="/admin" element={<AdminPage />} />
        </Route>

        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}
