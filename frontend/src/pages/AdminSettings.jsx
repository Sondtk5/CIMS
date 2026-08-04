import React, { useState, useEffect } from 'react';
import {
  Box, Card, CardContent, Typography, Table, TableHead, TableRow, TableCell, TableBody,
  TextField, Button, Alert, Snackbar, Paper, Grid, MenuItem
} from '@mui/material';
import { Save as SaveIcon, Settings as SettingsIcon } from '@mui/icons-material';
import { settingsAPI } from '../services/api';

export default function AdminSettings() {
  const [targets, setTargets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [savingKey, setSavingKey] = useState(null);
  const [msg, setMsg] = useState({ open: false, text: '', type: 'success' });

  const loadTargets = async () => {
    setLoading(true);
    try {
      const res = await settingsAPI.getKPITargets();
      setTargets(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadTargets();
  }, []);

  const handleValueChange = (kpiKey, val) => {
    setTargets(targets.map((t) => (t.kpi_key === kpiKey ? { ...t, target_value: parseFloat(val) || 0 } : t)));
  };

  const handleOperatorChange = (kpiKey, val) => {
    setTargets(targets.map((t) => (t.kpi_key === kpiKey ? { ...t, comparison_operator: val } : t)));
  };

  const handleSave = async (target) => {
    setSavingKey(target.kpi_key);
    try {
      await settingsAPI.updateKPITarget(target.kpi_key, {
        target_value: target.target_value,
        comparison_operator: target.comparison_operator,
        unit: target.unit
      });
      setMsg({ open: true, text: `Successfully updated target for ${target.kpi_name}`, type: 'success' });
      loadTargets();
    } catch (err) {
      setMsg({ open: true, text: err.response?.data?.detail || 'Failed to update target', type: 'error' });
    } finally {
      setSavingKey(null);
    }
  };

  return (
    <Box sx={{ p: 3 }}>
      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1.5, mb: 3 }}>
        <SettingsIcon color="primary" sx={{ fontSize: 32 }} />
        <Box>
          <Typography variant="h5" sx={{ fontWeight: 800 }}>Admin System Settings</Typography>
          <Typography variant="body2" sx={{ color: '#64748b' }}>Configure KPI Target thresholds for continuous improvement tracking</Typography>
        </Box>
      </Box>

      <Card sx={{ borderLeft: '4px solid #1565C0' }}>
        <CardContent>
          <Typography variant="h6" sx={{ fontWeight: 700, mb: 2 }}>KPI Target Configuration</Typography>
          
          <Table size="small">
            <TableHead>
              <TableRow sx={{ backgroundColor: '#f1f5f9' }}>
                <TableCell sx={{ fontWeight: 'bold' }}>KPI Metric Name</TableCell>
                <TableCell sx={{ fontWeight: 'bold' }}>Operator</TableCell>
                <TableCell sx={{ fontWeight: 'bold' }}>Target Threshold Value</TableCell>
                <TableCell sx={{ fontWeight: 'bold' }}>Unit</TableCell>
                <TableCell sx={{ fontWeight: 'bold' }}>Last Updated By</TableCell>
                <TableCell sx={{ fontWeight: 'bold' }}>Action</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {targets.map((t) => (
                <TableRow key={t.kpi_key} hover>
                  <TableCell sx={{ fontWeight: 600 }}>{t.kpi_name}</TableCell>
                  <TableCell sx={{ width: '120px' }}>
                    <TextField
                      select
                      size="small"
                      fullWidth
                      value={t.comparison_operator || '>='}
                      onChange={(e) => handleOperatorChange(t.kpi_key, e.target.value)}
                    >
                      <MenuItem value=">=">≥</MenuItem>
                      <MenuItem value="<=" fontStyle="italic">≤</MenuItem>
                      <MenuItem value="=">=</MenuItem>
                    </TextField>
                  </TableCell>
                  <TableCell sx={{ width: '180px' }}>
                    <TextField
                      type="number"
                      size="small"
                      fullWidth
                      value={t.target_value}
                      onChange={(e) => handleValueChange(t.kpi_key, e.target.value)}
                    />
                  </TableCell>
                  <TableCell>{t.unit}</TableCell>
                  <TableCell sx={{ color: '#64748b', fontSize: '0.85rem' }}>
                    {t.updated_by || 'System'} ({t.updated_at ? new Date(t.updated_at).toLocaleDateString() : 'Initial'})
                  </TableCell>
                  <TableCell>
                    <Button
                      variant="contained"
                      color="primary"
                      size="small"
                      startIcon={<SaveIcon />}
                      onClick={() => handleSave(t)}
                      disabled={savingKey === t.kpi_key}
                    >
                      {savingKey === t.kpi_key ? 'Saving...' : 'Save Target'}
                    </Button>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>

      <Snackbar open={msg.open} autoHideDuration={4000} onClose={() => setMsg({ ...msg, open: false })}>
        <Alert severity={msg.type} sx={{ width: '100%' }}>{msg.text}</Alert>
      </Snackbar>
    </Box>
  );
}
