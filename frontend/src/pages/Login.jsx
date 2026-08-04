import React, { useState } from 'react';
import {
  Box, Card, CardContent, Typography, TextField, Button, Alert, Chip, Divider, Grid
} from '@mui/material';
import { LockOutlined as LockIcon } from '@mui/icons-material';
import { useAuth } from '../context/AuthContext';

export default function Login() {
  const { login } = useAuth();
  const [username, setUsername] = useState('admin');
  const [password, setPassword] = useState('password123');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      await login(username, password);
    } catch (err) {
      setError(err.response?.data?.detail || 'Invalid login credentials');
    } finally {
      setLoading(false);
    }
  };

  const handleDemoSelect = (demoUser) => {
    setUsername(demoUser);
    setPassword('password123');
  };

  return (
    <Box sx={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', backgroundColor: '#0F172A' }}>
      <Card sx={{ maxWidth: 450, width: '100%', mx: 2, p: 2, boxShadow: '0 8px 32px rgba(0,0,0,0.3)' }}>
        <CardContent>
          <Box sx={{ textAlign: 'center', mb: 3 }}>
            <Box sx={{ display: 'inline-flex', backgroundColor: '#1565C0', color: '#fff', p: 1, borderRadius: 2, mb: 1 }}>
              <LockIcon sx={{ fontSize: 32 }} />
            </Box>
            <Typography variant="h5" sx={{ fontWeight: 800, color: '#0F172A' }}>
              CIMS Login
            </Typography>
            <Typography variant="caption" sx={{ color: '#64748b' }}>
              Continual Improvement Management System v1.0
            </Typography>
          </Box>

          {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}

          <form onSubmit={handleSubmit}>
            <TextField
              label="Username"
              fullWidth
              size="small"
              margin="normal"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
            <TextField
              label="Password"
              type="password"
              fullWidth
              size="small"
              margin="normal"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
            <Button
              type="submit"
              variant="contained"
              color="primary"
              fullWidth
              size="large"
              sx={{ mt: 2, mb: 2, fontWeight: 700 }}
              disabled={loading}
            >
              {loading ? 'Signing in...' : 'Sign In'}
            </Button>
          </form>

          <Divider sx={{ my: 2 }}>
            <Typography variant="caption" sx={{ color: '#94a3b8' }}>Demo Role Quick Login</Typography>
          </Divider>

          <Grid container spacing={1}>
            {[
              { role: 'Administrator', user: 'admin', color: 'primary' },
              { role: 'TPM Manager', user: 'manager', color: 'secondary' },
              { role: 'Engineer', user: 'engineer', color: 'info' },
              { role: 'QA Verifier', user: 'qa', color: 'success' },
              { role: 'Management', user: 'management', color: 'warning' },
              { role: 'Auditor', user: 'auditor', color: 'default' }
            ].map((d) => (
              <Grid item xs={6} key={d.user}>
                <Button
                  variant="outlined"
                  size="small"
                  fullWidth
                  onClick={() => handleDemoSelect(d.user)}
                  sx={{ fontSize: '0.7rem', py: 0.5 }}
                >
                  {d.role}
                </Button>
              </Grid>
            ))}
          </Grid>
        </CardContent>
      </Card>
    </Box>
  );
}
