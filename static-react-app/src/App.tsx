import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";
import DashboardLayout from "@/polymet/components/dashboard-layout";
import LoginPage from "@/polymet/pages/login-page";
import DashboardPage from "@/polymet/pages/dashboard-page";
import HistoricalPage from "@/polymet/pages/historical-page";

export default function CommoditiesCompassPrototype() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Navigate to="/login" replace />} />

        <Route path="/login" element={<LoginPage />} />

        <Route
          path="/dashboard"
          element={
            <DashboardLayout>
              <DashboardPage />
            </DashboardLayout>
          }
        />

        <Route
          path="/dashboard/historical"
          element={
            <DashboardLayout>
              <HistoricalPage />
            </DashboardLayout>
          }
        />
      </Routes>
    </Router>
  );
}
