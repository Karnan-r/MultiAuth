import { useEffect } from "react";
import { useNavigate } from "react-router-dom";

const Callback = () => {
  console.log("✅ Callback.tsx Loaded!");  // ⬅️ Force Debug Log

  const navigate = useNavigate();

  useEffect(() => {
    console.log("🔄 Inside useEffect in Callback.tsx!");

    const params = new URLSearchParams(window.location.search);
    const token = params.get("token");

    if (token) {
      console.log("🔑 Token found:", token);
      localStorage.setItem("jwt", token);
      console.log("✅ Token stored in localStorage:", localStorage.getItem("jwt"));

      setTimeout(() => {
        navigate("/dashboard");
      }, 1000);
    } else {
      console.error("❌ No token found in URL");
      navigate("/");
    }
  }, [navigate]);

  return <div>🔥 Callback Component Rendered! 🔥</div>;
};

export default Callback;
