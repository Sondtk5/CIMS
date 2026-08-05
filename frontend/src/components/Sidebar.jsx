import React from 'react';
import { Drawer, List, ListItem, ListItemButton, ListItemIcon, ListItemText, Box, Divider, Typography } from '@mui/material';
import {
  Dashboard as DashboardIcon,
  Assignment as ProjectIcon,
  Analytics as KPIIcon,
  Assessment as ReportIcon,
  History as AuditIcon,
  Settings as SettingsIcon
} from '@mui/icons-material';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const drawerWidth = 240;

export default function Sidebar() {
  const navigate = useNavigate();
  const location = useLocation();
  const { user } = useAuth();

  const navItems = [
    { text: 'Master Dashboard', icon: <DashboardIcon />, path: '/', roles: ['Administrator', 'TPM Manager', 'Engineer', 'QA Inspector', 'Management', 'Auditor'] },
    { text: 'CI Project Register', icon: <ProjectIcon />, path: '/projects', roles: ['Administrator', 'TPM Manager', 'Engineer', 'QA Inspector', 'Management', 'Auditor'] },
    { text: 'Reports & Analytics', icon: <ReportIcon />, path: '/reports', roles: ['Administrator', 'TPM Manager', 'Engineer', 'QA Inspector', 'Management', 'Auditor'] },
    { text: 'Log Tracking', icon: <AuditIcon />, path: '/audit', roles: ['Administrator', 'Auditor'] },
    { text: 'Admin Settings', icon: <SettingsIcon />, path: '/settings', roles: ['Administrator'] },
  ];

  const filteredItems = navItems.filter(item => user && item.roles.includes(user.role));

  return (
    <Drawer
      variant="permanent"
      sx={{
        width: drawerWidth,
        flexShrink: 0,
        '& .MuiDrawer-paper': {
          width: drawerWidth,
          boxSizing: 'border-box',
          top: 64, // below AppBar
          height: 'calc(100vh - 64px)',
          borderRight: '1px solid #e2e8f0'
        },
      }}
    >
      <Box sx={{ overflow: 'auto', p: 1.5 }}>
        <Typography variant="overline" sx={{ px: 2, color: '#94a3b8', fontWeight: 700, letterSpacing: 1 }}>
          Navigation
        </Typography>
        <List>
          {filteredItems.map((item) => {
            const active = location.pathname === item.path;
            return (
              <ListItem key={item.text} disablePadding sx={{ mb: 0.5 }}>
                <ListItemButton
                  selected={active}
                  onClick={() => navigate(item.path)}
                  sx={{
                    borderRadius: 1.5,
                    '&.Mui-selected': {
                      backgroundColor: '#1565C0',
                      color: '#ffffff',
                      '& .MuiListItemIcon-root': {
                        color: '#ffffff',
                      },
                      '&:hover': {
                        backgroundColor: '#0d47a1',
                      },
                    },
                  }}
                >
                  <ListItemIcon sx={{ minWidth: 40, color: active ? '#fff' : '#1565C0' }}>
                    {item.icon}
                  </ListItemIcon>
                  <ListItemText primary={item.text} primaryTypographyProps={{ fontSize: '0.9rem', fontWeight: active ? 700 : 500 }} />
                </ListItemButton>
              </ListItem>
            );
          })}
        </List>
      </Box>
    </Drawer>
  );
}
