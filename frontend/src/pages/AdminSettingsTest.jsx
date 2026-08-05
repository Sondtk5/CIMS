import React, { useState, useEffect } from 'react';
import { Box, Card, CardContent, Typography, Button, TextField, Switch, FormControlLabel, Grid, Alert, Snackbar } from '@mui/material';
import { Save as SaveIcon, Tune as TuneIcon } from '@mui/icons-material';
import { settingsAPI } from '../services/api';
import { useAuth } from '../context/AuthContext';

export default function AdminSettingsTest() {
  const { user } = useAuth();
  const isAdmin = user?.role === 'Administrator';

  const [ciParts, setCIParts] = useState([]);
  const [ciSeparator, setCISeparator] = useState('-');
  const [ciExample, setCIExample] = useState('');
  const [savingCI, setSavingCI] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [msg, setMsg] = useState({ open: false, text: '', type: 'success' });

  useEffect(() => {
    if (!isAdmin) {
      setError('Only administrators can access this page');
      setLoading(false);
      return;
    }

    loadCI();
  }, [isAdmin]);

  const loadCI = async () => {
    setLoading(true);
    setError('');
    try {
      const res = await settingsAPI.getCINumberingConfig();
      console.log('CI Config loaded:', res.data);
      setCIParts(res.data.parts || []);
      setCISeparator(res.data.separator || '-');
      setCIExample(res.data.example || '');
    } catch (err) {
      console.error('Error loading CI config:', err);
      setError(`Failed to load CI config: ${err.response?.data?.detail || err.message}`);
    } finally {
      setLoading(false);
    }
  };

  const handleCIPartToggle = (index) => {
    const updated = [...ciParts];
    updated[index].enabled = !updated[index].enabled;
    setCIParts(updated);
  };

  const handleCIPartValueChange = (index, value) => {
    const updated = [...ciParts];
    updated[index].value = value;
    setCIParts(updated);
  };

  const handleSaveCI = async () => {
    setSavingCI(true);
    try {
      const config_data = {
        parts: ciParts,
        separator: ciSeparator
      };
      const res = await settingsAPI.updateCINumberingConfig(config_data);
      setMsg({ open: true, text: 'CI numbering configuration saved successfully', type: 'success' });
      setCIExample(res.data.config.example);
    } catch (err) {
      setMsg({ open: true, text: err.response?.data?.detail || 'Failed to save CI configuration', type: 'error' });
    } finally {
      setSavingCI(false);
    }
  };

  if (!isAdmin) {
    return (
      <Box sx={{ p: 3 }}>
        <Alert severity="error">Only administrators can access this page</Alert>
      </Box>
    );
  }

  if (loading) {
    return (
      <Box sx={{ p: 3 }}>
        <Typography>Loading...</Typography>
      </Box>
    );
  }

  if (error) {
    return (
      <Box sx={{ p: 3 }}>
        <Alert severity="error">{error}</Alert>
        <Button variant="contained" onClick={loadCI} sx={{ mt: 2 }}>
          Retry
        </Button>
      </Box>
    );
  }

  return (
    <Box sx={{ p: 3 }}>
      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1.5, mb: 3 }}>
        <TuneIcon color="primary" sx={{ fontSize: 32 }} />
        <Box>
          <Typography variant="h5" sx={{ fontWeight: 800 }}>Admin Settings - CI Numbering</Typography>
          <Typography variant="body2" sx={{ color: '#64748b' }}>Configure CI Project Numbering Convention</Typography>
        </Box>
      </Box>

      <Grid container spacing={3}>
        {/* Config Panel */}
        <Grid item xs={12} md={7}>
          <Card sx={{ borderLeft: '4px solid #2563eb' }}>
            <CardContent>
              <Typography variant="h6" sx={{ fontWeight: 700, mb: 3 }}>Configuration</Typography>

              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1.5, mb: 3 }}>
                {ciParts.map((part, idx) => (
                  <Box key={idx} sx={{ display: 'flex', alignItems: 'center', gap: 2, p: 1.5, backgroundColor: '#f8fafc', borderRadius: 1 }}>
                    <FormControlLabel
                      control={
                        <Switch
                          checked={part.enabled}
                          onChange={() => handleCIPartToggle(idx)}
                          size="small"
                        />
                      }
                      label={<Typography sx={{ fontWeight: 600, minWidth: '100px' }}>{part.name}</Typography>}
                      sx={{ m: 0, flex: 0 }}
                    />
                    <TextField
                      label="Value"
                      size="small"
                      value={part.value}
                      onChange={(e) => handleCIPartValueChange(idx, e.target.value)}
                      disabled={!part.enabled}
                      sx={{ minWidth: '100px' }}
                    />
                    {part.auto_increment && (
                      <Typography variant="caption" sx={{ color: '#0891b2', backgroundColor: '#cffafe', px: 1, py: 0.5, borderRadius: 0.5, fontWeight: 600 }}>
                        AUTO-INCREMENT
                      </Typography>
                    )}
                  </Box>
                ))}
              </Box>

              <Box sx={{ mb: 3 }}>
                <Typography variant="subtitle2" sx={{ fontWeight: 700, mb: 1 }}>Separator</Typography>
                <TextField
                  label="Separator"
                  size="small"
                  value={ciSeparator}
                  onChange={(e) => setCISeparator(e.target.value)}
                  sx={{ width: '150px' }}
                />
              </Box>

              <Button
                variant="contained"
                color="primary"
                startIcon={<SaveIcon />}
                onClick={handleSaveCI}
                disabled={savingCI}
                fullWidth
              >
                {savingCI ? 'Saving...' : 'Save Configuration'}
              </Button>
            </CardContent>
          </Card>
        </Grid>

        {/* Preview Panel */}
        <Grid item xs={12} md={5}>
          <Card sx={{ borderLeft: '4px solid #059669', backgroundColor: '#f0fdf4' }}>
            <CardContent>
              <Typography variant="h6" sx={{ fontWeight: 700, mb: 3 }}>Preview</Typography>
              
              <Box sx={{ mb: 3, p: 2, backgroundColor: '#fff', border: '2px dashed #059669', borderRadius: 1 }}>
                <Typography variant="caption" sx={{ color: '#64748b' }}>Next CI Number:</Typography>
                <Typography variant="h5" sx={{ fontWeight: 800, fontFamily: 'monospace', color: '#059669', mt: 1 }}>
                  {ciExample}
                </Typography>
              </Box>

              <Box sx={{ p: 2, backgroundColor: '#f0fdf4', border: '1px solid #dcfce7', borderRadius: 1 }}>
                <Typography variant="subtitle2" sx={{ fontWeight: 700, mb: 1, color: '#065f46' }}>Format Guide:</Typography>
                <Box component="ul" sx={{ m: 0, pl: 2, color: '#047857' }}>
                  <li><Typography variant="caption">Enabled parts: Will appear in CI number</Typography></li>
                  <li><Typography variant="caption">Toggle: Turn parts ON/OFF to customize</Typography></li>
                  <li><Typography variant="caption">Auto-increment: Counter increases with each project</Typography></li>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      <Snackbar open={msg.open} autoHideDuration={4000} onClose={() => setMsg({ ...msg, open: false })}>
        <Alert severity={msg.type}>{msg.text}</Alert>
      </Snackbar>
    </Box>
  );
}
