import { BrowserRouter, Routes, Route } from "react-router-dom";
import Login from "./pages/Login";
import Signup from "./pages/Signup";
import Dashboard from "./pages/Dashboard";
import Callback from "./pages/Callback";

const AppRoutes = () => {
  console.log("✅ AppRoutes Loaded!");

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/oauth/callback" element={<Callback />} />
      </Routes>
    </BrowserRouter>
  );
};

export default AppRoutes;
