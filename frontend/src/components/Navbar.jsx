import React from 'react';
import {
  AppBar, Toolbar, Typography, Box, IconButton, Button, Chip, Avatar, Tooltip
} from '@mui/material';
import {
  Brightness4, Brightness7, Logout as LogoutIcon, Person as PersonIcon, AdminPanelSettings as AdminIcon
} from '@mui/icons-material';
import { useAuth } from '../context/AuthContext';

export default function Navbar({ darkMode, setDarkMode }) {
  const { user, logout } = useAuth();

  return (
    <AppBar position="sticky" color="default" elevation={1} sx={{ backgroundColor: darkMode ? '#0f172a' : '#ffffff', borderBottom: '1px solid #e2e8f0' }}>
      <Toolbar sx={{ justifyContent: 'space-between' }}>
        {/* Left: Logo & App Title */}
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
          {/* UTI Logo Box matching image template */}
          <Box sx={{
            backgroundColor: '#0F172A',
            color: '#ffffff',
            fontWeight: 800,
            fontSize: '1.2rem',
            padding: '4px 12px',
            borderRadius: 1,
            display: 'flex',
            alignItems: 'center',
            gap: 0.5,
            borderLeft: '4px solid #1565C0'
          }}>
            UTI
            <Typography variant="caption" sx={{ color: '#94a3b8', fontSize: '0.65rem', display: 'block', lineHeight: 1 }}>
              Unique Tech Integral
            </Typography>
          </Box>
          <Box>
            <Typography variant="h6" sx={{ fontWeight: 700, fontSize: '1.1rem', color: darkMode ? '#fff' : '#0f172a' }}>
              CONTINUAL IMPROVEMENT MANAGEMENT SYSTEM (CIMS)
            </Typography>
            <Typography variant="caption" sx={{ color: '#64748b' }}>
              ISO 9001:2015 Clause 10.3 | IATF 16949 | TPM Department
            </Typography>
          </Box>
        </Box>

        {/* Right: Controls & User Profile */}
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
          {user && (
            <Chip
              icon={<AdminIcon />}
              label={`${user.full_name} (${user.role})`}
              color="primary"
              variant="outlined"
              size="small"
              sx={{ fontWeight: 600 }}
            />
          )}

          <Tooltip title={darkMode ? 'Switch to Light Mode' : 'Switch to Dark Mode'}>
            <IconButton onClick={() => setDarkMode(!darkMode)} color="inherit" size="small">
              {darkMode ? <Brightness7 color="warning" /> : <Brightness4 />}
            </IconButton>
          </Tooltip>

          {user && (
            <Button
              variant="outlined"
              color="error"
              size="small"
              startIcon={<LogoutIcon />}
              onClick={logout}
            >
              Logout
            </Button>
          )}
        </Box>
      </Toolbar>
    </AppBar>
  );
}
