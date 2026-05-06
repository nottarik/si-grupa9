import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";
import type { User } from "../types";

/* ── Sign In Form ── */
interface FormProps {
  onSwitch: () => void;
  onSuccess: (user: User) => void;
}

function SignIn({ onSwitch, onSuccess }: FormProps) {
  const { login } = useAuth();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPass, setShowPass] = useState(false);
  const [remember, setRemember] = useState(false);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      const user = await login(email, password);
      onSuccess(user);
    } catch {
      setError("Pogrešan email ili lozinka.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-5">
      <div>
        <label className="block text-xs font-semibold tracking-widest uppercase mb-1.5" style={{ color: "#5a4a30" }}>
          Email Address
        </label>
        <input
          className="input-field"
          type="email"
          placeholder="you@organization.com"
          required
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
      </div>

      <div>
        <div className="flex justify-between items-center mb-1.5">
          <label className="text-xs font-semibold tracking-widest uppercase" style={{ color: "#5a4a30" }}>
            Password
          </label>
          <button type="button" className="link-btn text-xs">Forgot password?</button>
        </div>
        <div className="relative">
          <input
            className="input-field"
            type={showPass ? "text" : "password"}
            placeholder="Enter your password"
            required
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            style={{ paddingRight: 40 }}
          />
          <button
            type="button"
            onClick={() => setShowPass((v) => !v)}
            className="absolute right-3 top-1/2 -translate-y-1/2 text-xs"
            style={{ color: "#9a8a6a", background: "none", border: "none", cursor: "pointer" }}
          >
            {showPass ? "Hide" : "Show"}
          </button>
        </div>
      </div>

      <div className="flex items-center gap-2">
        <input
          type="checkbox"
          id="remember"
          className="w-4 h-4"
          checked={remember}
          onChange={(e) => setRemember(e.target.checked)}
          style={{ accentColor: "#C5A059" }}
        />
        <label htmlFor="remember" className="text-sm" style={{ color: "#5a4a30" }}>
          Keep me signed in
        </label>
      </div>

      {error && <p className="text-xs" style={{ color: "#c62828" }}>{error}</p>}

      <button type="submit" className="gold-btn" style={{ width: "100%", padding: "11px 18px" }} disabled={loading}>
        {loading ? "Signing in…" : "Sign In"}
      </button>

      <div className="divider-or">or</div>

      <button type="button" className="ghost-btn" onClick={onSwitch}>
        Create an Account
      </button>
    </form>
  );
}

/* ── Sign Up Form ── */
function SignUp({ onSwitch, onSuccess }: FormProps) {
  const { register } = useAuth();
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPass, setConfirmPass] = useState("");
  const [showPass, setShowPass] = useState(false);
  const [terms, setTerms] = useState(false);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!firstName || !email || !password || !confirmPass) {
      setError("Please fill in all required fields.");
      return;
    }
    if (password.length < 8) {
      setError("Password must be at least 8 characters.");
      return;
    }
    if (password !== confirmPass) {
      setError("Passwords do not match.");
      return;
    }
    if (!terms) {
      setError("You must accept the Terms of Service.");
      return;
    }
    setError("");
    setLoading(true);
    try {
      const fullName = lastName ? `${firstName} ${lastName}` : firstName;
      const user = await register({ email, password, full_name: fullName });
      onSuccess(user);
    } catch (err: unknown) {
      const detail = (err as { response?: { data?: { detail?: string } } })?.response?.data?.detail;
      if (detail === "Email already registered") {
        setError("This email is already registered. Please sign in.");
      } else {
        setError("Registration failed. Please try again.");
      }
    } finally {
      setLoading(false);
    }
  }

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-4">
      <div className="grid grid-cols-2 gap-3">
        <div>
          <label className="block text-xs font-semibold tracking-widest uppercase mb-1.5" style={{ color: "#5a4a30" }}>
            First Name
          </label>
          <input
            className="input-field"
            placeholder="First name"
            required
            value={firstName}
            onChange={(e) => setFirstName(e.target.value)}
          />
        </div>
        <div>
          <label className="block text-xs font-semibold tracking-widest uppercase mb-1.5" style={{ color: "#5a4a30" }}>
            Last Name
          </label>
          <input
            className="input-field"
            placeholder="Last name"
            value={lastName}
            onChange={(e) => setLastName(e.target.value)}
          />
        </div>
      </div>

      <div>
        <label className="block text-xs font-semibold tracking-widest uppercase mb-1.5" style={{ color: "#5a4a30" }}>
          Email Address
        </label>
        <input
          className="input-field"
          type="email"
          placeholder="you@organization.com"
          required
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
      </div>

      <div>
        <label className="block text-xs font-semibold tracking-widest uppercase mb-1.5" style={{ color: "#5a4a30" }}>
          Password
        </label>
        <div className="relative">
          <input
            className="input-field"
            type={showPass ? "text" : "password"}
            placeholder="Min. 8 characters"
            required
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            style={{ paddingRight: 40 }}
          />
          <button
            type="button"
            onClick={() => setShowPass((v) => !v)}
            className="absolute right-3 top-1/2 -translate-y-1/2 text-xs"
            style={{ color: "#9a8a6a", background: "none", border: "none", cursor: "pointer" }}
          >
            {showPass ? "Hide" : "Show"}
          </button>
        </div>
      </div>

      <div>
        <label className="block text-xs font-semibold tracking-widest uppercase mb-1.5" style={{ color: "#5a4a30" }}>
          Confirm Password
        </label>
        <input
          className="input-field"
          type="password"
          placeholder="Repeat password"
          required
          value={confirmPass}
          onChange={(e) => setConfirmPass(e.target.value)}
        />
      </div>

      <div className="flex items-start gap-2 pt-1">
        <input
          type="checkbox"
          id="terms"
          className="w-4 h-4 mt-0.5"
          checked={terms}
          onChange={(e) => setTerms(e.target.checked)}
          style={{ accentColor: "#C5A059" }}
        />
        <label htmlFor="terms" className="text-sm leading-relaxed" style={{ color: "#5a4a30" }}>
          I agree to the{" "}
          <button type="button" className="link-btn">Terms of Service</button>
          {" "}and{" "}
          <button type="button" className="link-btn">Privacy Policy</button>
        </label>
      </div>

      {error && <p className="text-xs" style={{ color: "#c62828" }}>{error}</p>}

      <button type="submit" className="gold-btn" style={{ width: "100%", padding: "11px 18px" }} disabled={loading}>
        {loading ? "Creating account…" : "Create Account"}
      </button>

      <div className="divider-or">or</div>

      <button type="button" className="ghost-btn" onClick={onSwitch}>
        Sign In to Existing Account
      </button>
    </form>
  );
}

/* ── LoginPage ── */
export default function LoginPage() {
  const [mode, setMode] = useState<"signin" | "signup">("signin");
  const navigate = useNavigate();

  function handleSuccess(user: User) {
    navigate(user.role === "admin" ? "/admin" : "/chat", { replace: true });
  }

  return (
    <div className="admin-bg min-h-screen overflow-y-auto flex items-center justify-center px-6 py-12">
      <div className="w-full" style={{ maxWidth: 400 }}>

        {/* Header */}
        <div className="text-center mb-7">
          <div className="coin-logo mb-4">A</div>
          <h1 className="font-cinzel font-bold tracking-[0.15em] text-charcoal" style={{ fontSize: 20 }}>
            {mode === "signin" ? "Welcome Back" : "Create Account"}
          </h1>
          <p className="text-sm mt-1.5" style={{ color: "#6b5a3a" }}>
            {mode === "signin"
              ? "Sign in to access the Ambassador AI chatbot."
              : "Register to join the Ambassador platform."}
          </p>
        </div>

        {/* Toggle */}
        <div className="auth-toggle mb-6">
          <button
            type="button"
            className={mode === "signin" ? "on" : ""}
            onClick={() => setMode("signin")}
          >
            Sign In
          </button>
          <button
            type="button"
            className={mode === "signup" ? "on" : ""}
            onClick={() => setMode("signup")}
          >
            Sign Up
          </button>
        </div>

        {/* Card */}
        <div className="card p-7">
          {mode === "signin" ? (
            <SignIn onSwitch={() => setMode("signup")} onSuccess={handleSuccess} />
          ) : (
            <SignUp onSwitch={() => setMode("signin")} onSuccess={handleSuccess} />
          )}
        </div>

      </div>
    </div>
  );
}
