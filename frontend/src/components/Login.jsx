import { useState } from "react";
import api from "../api";
import qs from "qs";

export default function Login({ onLogin }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      const response = await api.post(
        "/auth/login",
        qs.stringify({
          username: email,
          password: password,
        }),
        {
          headers: { "Content-Type": "application/x-www-form-urlencoded" },
        }
      );
      console.log("Login response:", response.data);
      
      const token = response.data.access_token;
      localStorage.setItem("token", token);
      onLogin(token);
    } catch (err) {
        console.error("Login error:", err);
        setError("Login failed. See console for details.");
    }
    finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <div className="card">
        <h1>Login</h1>
        <form onSubmit={handleSubmit}>
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          {error && <p style={{ color: "red", marginBottom: "1rem" }}>{error}</p>}
          <button type="submit" disabled={loading}>
            {loading ? "Logging in…" : "Login"}
          </button>
        </form>
      </div>
    </div>
  );
}
