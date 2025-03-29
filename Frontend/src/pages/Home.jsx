// Home page component with navigation and post display
import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import Posts from "../components/Posts";

const Home = () => {
  const [logoutError, setLogoutError] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      navigate("/login");
    }
  }, [navigate]);

  const handleLogout = async () => {
    try {
      const token = localStorage.getItem("token");
      if (!token) {
        localStorage.removeItem("token");
        navigate("/login", { replace: true });
        return;
      }

      await axios.post(
        "http://localhost:5000/logout",
        {},
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );
      localStorage.removeItem("token");
      navigate("/login", { replace: true });
    } catch (error) {
      console.error("Logout failed:", error.response?.data || error);
      setLogoutError(error.response?.data?.message || "Logout failed");
      // Still remove token and redirect on error
      localStorage.removeItem("token");
      navigate("/login", { replace: true });
    }
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <nav className="bg-white shadow-md p-4 mb-6">
        <div className="max-w-7xl mx-auto flex justify-between items-center">
          <h1 className="text-2xl font-bold">Nested Comments</h1>
          <div className="flex items-center gap-4">
            {logoutError && (
              <span className="text-red-500 text-sm">{logoutError}</span>
            )}
            <button
              onClick={handleLogout}
              className="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600"
            >
              Logout
            </button>
          </div>
        </div>
      </nav>

      <main className="container mx-auto px-4 py-8">
        <Posts />
      </main>
    </div>
  );
};

export default Home;
