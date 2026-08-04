import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ThemeProvider, CssBaseline, Box } from '@mui/material';
import { getAppTheme } from './theme';
import { AuthProvider, useAuth } from './context/AuthContext';

import Navbar from './components/Navbar';
import Sidebar from './components/Sidebar';
import MasterDashboard from './pages/MasterDashboard';
import ProjectRegister from './pages/ProjectRegister';
import AdminSettings from './pages/AdminSettings';
import Reports from './pages/Reports';
import AuditLogs from './pages/AuditLogs';
import Login from './pages/Login';

function ProtectedLayout({ darkMode, setDarkMode }) {
  const { user, loading } = useAuth();

  if (loading) return null;
  if (!user) return <Navigate to="/login" replace />;

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      <Navbar darkMode={darkMode} setDarkMode={setDarkMode} />
      <Box sx={{ display: 'flex', flexGrow: 1 }}>
        <Sidebar />
        <Box component="main" sx={{ flexGrow: 1, backgroundColor: darkMode ? '#0f172a' : '#f4f6f9', minHeight: 'calc(100vh - 64px)' }}>
          <Routes>
            <Route path="/" element={<MasterDashboard />} />
            <Route path="/projects" element={<ProjectRegister />} />
            <Route path="/settings" element={<AdminSettings />} />
            <Route path="/reports" element={<Reports />} />
            <Route path="/audit" element={<AuditLogs />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </Box>
      </Box>
    </Box>
  );
}

export default function App() {
  const [darkMode, setDarkMode] = useState(false);
  const theme = getAppTheme(darkMode ? 'dark' : 'light');

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <AuthProvider>
        <Router>
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route path="/*" element={<ProtectedLayout darkMode={darkMode} setDarkMode={setDarkMode} />} />
          </Routes>
        </Router>
      </AuthProvider>
    </ThemeProvider>
  );
}
