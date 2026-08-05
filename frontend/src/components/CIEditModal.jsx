import React, { useState, useEffect } from 'react';
import {
  Dialog, DialogTitle, DialogContent, DialogActions, Button, Tabs, Tab, Box, Typography,
  TextField, MenuItem, Grid, Card, CardContent, Table, TableHead, TableRow, TableCell,
  TableBody, Chip, IconButton, Alert, Divider, Skeleton
} from '@mui/material';
import {
  Close as CloseIcon, Print as PrintIcon, Save as SaveIcon, Delete as DeleteIcon, Add as AddIcon, Refresh as RefreshIcon
} from '@mui/icons-material';
import CIRequestFormPrintView from './CIRequestFormPrintView';
import CIReportPrintView from './CIReportPrintView';
import { projectsAPI, settingsAPI } from '../services/api';

export default function CIEditModal({ open, onClose, project, onSaved, onDelete }) {
  const [activeTab, setActiveTab] = useState(0);
  const [printMode, setPrintMode] = useState(null); // 'request' or 'report' or null
  const [formData, setFormData] = useState({});
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');
  const [generatingCI, setGeneratingCI] = useState(false);

  useEffect(() => {
    if (project) {
      setFormData({
        ...project,
        define_stage: project.define_stage || {},
        measure_stage: project.measure_stage || {},
        analyze_stage: project.analyze_stage || { five_why: [] },
        improve_stage: project.improve_stage || {},
        control_stage: project.control_stage || {},
      });
      // Auto-generate CI if it's a new project (no id)
      if (!project.id && !project.ci_no) {
        generateNewCI();
      }
    }
  }, [project]);

  const generateNewCI = async () => {
    setGeneratingCI(true);
    try {
      const res = await settingsAPI.getCINumberingConfig();
      const example = res.data.example || 'AUTO';
      setFormData((prev) => ({ ...prev, ci_no: example }));
    } catch (err) {
      console.error('Failed to generate CI:', err);
    } finally {
      setGeneratingCI(false);
    }
  };

  if (!project) return null;

  const handleChange = (field, value) => {
    setFormData((prev) => ({ ...prev, [field]: value }));
  };

  const handleSave = async () => {
    setSaving(true);
    setError('');
    try {
      if (formData.id) {
        await projectsAPI.update(formData.id, formData);
      } else {
        await projectsAPI.create(formData);
      }
      onSaved();
      onClose();
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to save project');
    } finally {
      setSaving(false);
    }
  };

  const handlePrint = (type) => {
    setPrintMode(type);
    setTimeout(() => {
      window.print();
      setPrintMode(null);
    }, 300);
  };

  return (
    <Dialog open={open} onClose={onClose} maxWidth="md" fullWidth>
      <DialogTitle sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', backgroundColor: '#0F172A', color: '#fff', py: 1.5 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1.5 }}>
          <Chip label={formData.ci_no || 'NEW'} color="primary" sx={{ fontWeight: 800 }} />
          <Typography variant="h6" sx={{ fontWeight: 700, fontSize: '1.1rem' }}>
            {formData.title || 'CI Project Workspace'}
          </Typography>
        </Box>
        <Box sx={{ display: 'flex', gap: 1 }}>
          <Button variant="contained" color="info" size="small" startIcon={<PrintIcon />} onClick={() => handlePrint('request')}>
            Print Request Form
          </Button>
          <Button variant="contained" color="secondary" size="small" startIcon={<PrintIcon />} onClick={() => handlePrint('report')}>
            Print DMAIC Report
          </Button>
          <IconButton color="inherit" onClick={onClose} size="small">
            <CloseIcon />
          </IconButton>
        </Box>
      </DialogTitle>

      {/* Tabs */}
      <Box sx={{ borderBottom: 1, borderColor: 'divider', backgroundColor: '#f8fafc' }}>
        <Tabs value={activeTab} onChange={(e, val) => setActiveTab(val)} variant="scrollable" scrollButtons="auto">
          <Tab label="1. General & Request Form" />
          <Tab label="2. DMAIC Project Report" />
          <Tab label="3. Root Cause (5-Why)" />
          <Tab label="4. Verification & Cost Saving" />
          <Tab label="5. TPM Review & Approval" />
        </Tabs>
      </Box>

      <DialogContent dividers sx={{ p: 3 }}>
        {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}

        {/* TAB 0: General & Request Form */}
        {activeTab === 0 && (
          <Grid container spacing={2}>
            <Grid item xs={6}>
              <Box sx={{ display: 'flex', gap: 1, alignItems: 'flex-end' }}>
                <TextField 
                  label="CI No." 
                  fullWidth 
                  size="small" 
                  value={generatingCI ? 'Generating...' : (formData.ci_no || '')} 
                  disabled 
                  sx={{ flex: 1 }}
                />
                {!formData.id && (
                  <Button 
                    variant="outlined" 
                    size="small" 
                    startIcon={<RefreshIcon />}
                    onClick={generateNewCI}
                    disabled={generatingCI}
                    sx={{ mb: 0.75 }}
                  >
                    Auto
                  </Button>
                )}
              </Box>
            </Grid>
            <Grid item xs={6}>
              <TextField label="Project Title" fullWidth size="small" value={formData.title || ''} onChange={(e) => handleChange('title', e.target.value)} />
            </Grid>
            <Grid item xs={6}>
              <TextField label="Department" fullWidth size="small" value={formData.department || ''} onChange={(e) => handleChange('department', e.target.value)} />
            </Grid>
            <Grid item xs={6}>
              <TextField label="Process / Area" fullWidth size="small" value={formData.process_area || ''} onChange={(e) => handleChange('process_area', e.target.value)} />
            </Grid>
            <Grid item xs={6}>
              <TextField select label="Category" fullWidth size="small" value={formData.category || 'Quality'} onChange={(e) => handleChange('category', e.target.value)}>
                {['Quality', 'Productivity', 'Cost Saving', 'Equipment', 'Safety / Environment', 'Others'].map((cat) => (
                  <MenuItem key={cat} value={cat}>{cat}</MenuItem>
                ))}
              </TextField>
            </Grid>
            <Grid item xs={6}>
              <TextField select label="Priority" fullWidth size="small" value={formData.priority || 'Medium'} onChange={(e) => handleChange('priority', e.target.value)}>
                <MenuItem value="High">High</MenuItem>
                <MenuItem value="Medium">Medium</MenuItem>
                <MenuItem value="Low">Low</MenuItem>
              </TextField>
            </Grid>
            <Grid item xs={6}>
              <TextField label="Owner / Project Leader" fullWidth size="small" value={formData.owner || ''} onChange={(e) => handleChange('owner', e.target.value)} />
            </Grid>
            <Grid item xs={6}>
              <TextField label="Requester" fullWidth size="small" value={formData.requester || ''} onChange={(e) => handleChange('requester', e.target.value)} />
            </Grid>
            <Grid item xs={4}>
              <TextField type="date" label="Start Date" InputLabelProps={{ shrink: true }} fullWidth size="small" value={formData.start_date || ''} onChange={(e) => handleChange('start_date', e.target.value)} />
            </Grid>
            <Grid item xs={4}>
              <TextField type="date" label="Target Due Date" InputLabelProps={{ shrink: true }} fullWidth size="small" value={formData.due_date || ''} onChange={(e) => handleChange('due_date', e.target.value)} />
            </Grid>
            <Grid item xs={4}>
              <TextField type="date" label="Close Date" InputLabelProps={{ shrink: true }} fullWidth size="small" value={formData.close_date || ''} onChange={(e) => handleChange('close_date', e.target.value)} />
            </Grid>
            <Grid item xs={6}>
              <TextField select label="Status" fullWidth size="small" value={formData.status || 'Running'} onChange={(e) => handleChange('status', e.target.value)}>
                <MenuItem value="Complete">Complete</MenuItem>
                <MenuItem value="Running">Running</MenuItem>
                <MenuItem value="Pending">Pending</MenuItem>
              </TextField>
            </Grid>
            <Grid item xs={6}>
              <TextField label="Progress (%)" type="number" fullWidth size="small" value={formData.progress ?? 0} onChange={(e) => handleChange('progress', parseInt(e.target.value))} />
            </Grid>
            <Grid item xs={12}>
              <TextField label="Issue Description" multiline rows={2} fullWidth size="small" value={formData.issue_description || ''} onChange={(e) => handleChange('issue_description', e.target.value)} />
            </Grid>
            <Grid item xs={12}>
              <TextField label="Current Status" multiline rows={2} fullWidth size="small" value={formData.current_status || ''} onChange={(e) => handleChange('current_status', e.target.value)} />
            </Grid>
          </Grid>
        )}

        {/* TAB 1: DMAIC Project Report */}
        {activeTab === 1 && (
          <Grid container spacing={2}>
            <Grid item xs={12}>
              <Typography variant="subtitle2" sx={{ fontWeight: 'bold', color: '#1565C0', mb: 1 }}>DMAIC Stage Summaries</Typography>
            </Grid>
            <Grid item xs={6}>
              <TextField label="Define Stage Summary" multiline rows={2} fullWidth size="small" value={formData.define_stage?.summary || ''} onChange={(e) => handleChange('define_stage', { ...formData.define_stage, summary: e.target.value })} />
            </Grid>
            <Grid item xs={6}>
              <TextField label="Measure Stage Summary" multiline rows={2} fullWidth size="small" value={formData.measure_stage?.summary || ''} onChange={(e) => handleChange('measure_stage', { ...formData.measure_stage, summary: e.target.value })} />
            </Grid>
            <Grid item xs={6}>
              <TextField label="Improve Stage Summary" multiline rows={2} fullWidth size="small" value={formData.improve_stage?.summary || ''} onChange={(e) => handleChange('improve_stage', { ...formData.improve_stage, summary: e.target.value })} />
            </Grid>
            <Grid item xs={6}>
              <TextField label="Control & Standardize Summary" multiline rows={2} fullWidth size="small" value={formData.control_stage?.summary || ''} onChange={(e) => handleChange('control_stage', { ...formData.control_stage, summary: e.target.value })} />
            </Grid>
          </Grid>
        )}

        {/* TAB 2: Root Cause (5-Why) */}
        {activeTab === 2 && (
          <Box>
            <Typography variant="subtitle2" sx={{ fontWeight: 'bold', color: '#1565C0', mb: 2 }}>
              5-Why Root Cause Analysis Tree
            </Typography>
            <Table size="small" sx={{ mb: 2 }}>
              <TableHead>
                <TableRow>
                  <TableCell sx={{ width: '10%' }}>Step</TableCell>
                  <TableCell sx={{ width: '45%' }}>Why Question</TableCell>
                  <TableCell sx={{ width: '45%' }}>Answer / Cause</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {[1, 2, 3, 4, 5].map((step, idx) => (
                  <TableRow key={step}>
                    <TableCell sx={{ fontWeight: 'bold' }}>Why {step}</TableCell>
                    <TableCell>
                      <TextField size="small" fullWidth placeholder={`Why ${step}...`} value={formData.analyze_stage?.five_why?.[idx]?.why || ''} onChange={(e) => {
                        const fw = [...(formData.analyze_stage?.five_why || [])];
                        fw[idx] = { ...fw[idx], why: e.target.value };
                        handleChange('analyze_stage', { ...formData.analyze_stage, five_why: fw });
                      }} />
                    </TableCell>
                    <TableCell>
                      <TextField size="small" fullWidth placeholder="Root cause answer..." value={formData.analyze_stage?.five_why?.[idx]?.answer || ''} onChange={(e) => {
                        const fw = [...(formData.analyze_stage?.five_why || [])];
                        fw[idx] = { ...fw[idx], answer: e.target.value };
                        handleChange('analyze_stage', { ...formData.analyze_stage, five_why: fw });
                      }} />
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </Box>
        )}

        {/* TAB 3: Verification & Cost Saving */}
        {activeTab === 3 && (
          <Grid container spacing={2}>
            <Grid item xs={6}>
              <TextField label="KPI Metric Name" fullWidth size="small" placeholder="Defect Rate (%), UPH, etc." value={formData.kpi_metric || ''} onChange={(e) => handleChange('kpi_metric', e.target.value)} />
            </Grid>
            <Grid item xs={6}>
              <TextField select label="QA Verification Result" fullWidth size="small" value={formData.result || '-'} onChange={(e) => handleChange('result', e.target.value)}>
                <MenuItem value="PASS">PASS</MenuItem>
                <MenuItem value="FAIL">FAIL</MenuItem>
                <MenuItem value="-">-</MenuItem>
              </TextField>
            </Grid>
            <Grid item xs={4}>
              <TextField type="number" label="Before Value" fullWidth size="small" value={formData.before_value ?? ''} onChange={(e) => handleChange('before_value', parseFloat(e.target.value))} />
            </Grid>
            <Grid item xs={4}>
              <TextField type="number" label="Target Value" fullWidth size="small" value={formData.target_value ?? ''} onChange={(e) => handleChange('target_value', parseFloat(e.target.value))} />
            </Grid>
            <Grid item xs={4}>
              <TextField type="number" label="After Value" fullWidth size="small" value={formData.after_value ?? ''} onChange={(e) => handleChange('after_value', parseFloat(e.target.value))} />
            </Grid>
            <Grid item xs={6}>
              <TextField type="number" label="Cost Saving ($ USD/Year)" fullWidth size="small" value={formData.cost_saving ?? 0} onChange={(e) => handleChange('cost_saving', parseFloat(e.target.value))} />
            </Grid>
            <Grid item xs={6}>
              <TextField select label="Horizontal Deployment (Yokoten)" fullWidth size="small" value={formData.horizontal_deploy || 'No'} onChange={(e) => handleChange('horizontal_deploy', e.target.value)}>
                <MenuItem value="Yes">Yes</MenuItem>
                <MenuItem value="No">No</MenuItem>
              </TextField>
            </Grid>
          </Grid>
        )}

        {/* TAB 4: TPM Review & Approval */}
        {activeTab === 4 && (
          <Grid container spacing={2}>
            <Grid item xs={6}>
              <TextField label="Reviewed By" fullWidth size="small" value={formData.tpm_reviewed_by || ''} onChange={(e) => handleChange('tpm_reviewed_by', e.target.value)} />
            </Grid>
            <Grid item xs={6}>
              <TextField type="date" label="Review Date" InputLabelProps={{ shrink: true }} fullWidth size="small" value={formData.tpm_review_date || ''} onChange={(e) => handleChange('tpm_review_date', e.target.value)} />
            </Grid>
            <Grid item xs={12}>
              <TextField label="Review Comment" multiline rows={2} fullWidth size="small" value={formData.tpm_review_comment || ''} onChange={(e) => handleChange('tpm_review_comment', e.target.value)} />
            </Grid>
            <Grid item xs={6}>
              <TextField select label="TPM Decision" fullWidth size="small" value={formData.tpm_decision || 'Approved'} onChange={(e) => handleChange('tpm_decision', e.target.value)}>
                <MenuItem value="Approved">Approved</MenuItem>
                <MenuItem value="Not Approved">Not Approved</MenuItem>
                <MenuItem value="Pending">Pending</MenuItem>
              </TextField>
            </Grid>
          </Grid>
        )}
      </DialogContent>

      <DialogActions sx={{ px: 3, py: 2, backgroundColor: '#f8fafc', justifyContent: 'space-between' }}>
        {formData.id ? (
          <Button variant="outlined" color="error" startIcon={<DeleteIcon />} onClick={() => onDelete(formData.id)}>
            Delete Project
          </Button>
        ) : <Box />}
        <Box sx={{ display: 'flex', gap: 1 }}>
          <Button variant="outlined" onClick={onClose}>Cancel</Button>
          <Button variant="contained" color="primary" startIcon={<SaveIcon />} onClick={handleSave} disabled={saving}>
            {saving ? 'Saving...' : 'Save Changes'}
          </Button>
        </Box>
      </DialogActions>

      {/* Hidden printable elements rendered when user clicks print */}
      <Box sx={{ display: printMode ? 'block' : 'none' }}>
        {printMode === 'request' && <CIRequestFormPrintView project={formData} />}
        {printMode === 'report' && <CIReportPrintView project={formData} />}
      </Box>
    </Dialog>
  );
}
