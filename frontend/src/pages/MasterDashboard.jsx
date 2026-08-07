import React, { useState, useEffect } from 'react';
import {
  Box, Grid, Card, CardContent, Typography, Table, TableHead, TableRow, TableCell,
  TableBody, Chip, Button, IconButton, TextField, MenuItem, CircularProgress, Alert, useTheme
} from '@mui/material';
import {
  FolderSpecial as TotalIcon,
  CheckCircle as CompleteIcon,
  Settings as RunningIcon,
  HourglassEmpty as PendingIcon,
  Speed as RateIcon,
  Savings as CostIcon,
  Share as HorizontalIcon,
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  FileDownload as ExportIcon
} from '@mui/icons-material';
import ReactECharts from 'echarts-for-react';
import { dashboardAPI, projectsAPI } from '../services/api';
import CIEditModal from '../components/CIEditModal';
import * as XLSX from 'xlsx';

export default function MasterDashboard() {
  const theme = useTheme();
  const isDark = theme.palette.mode === 'dark';
  const [data, setData] = useState(null);
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedProject, setSelectedProject] = useState(null);
  const [modalOpen, setModalOpen] = useState(false);
  const [selectedYear, setSelectedYear] = useState(new Date().getFullYear());
  const [availableYears, setAvailableYears] = useState([new Date().getFullYear()]);

  // Load available years on component mount
  useEffect(() => {
    const loadYears = async () => {
      try {
        const res = await dashboardAPI.getAvailableYears();
        if (res.data && res.data.years) {
          setAvailableYears(res.data.years);
        }
      } catch (err) {
        console.warn('Failed to load available years', err);
        // Fallback to default years
        setAvailableYears([2024, 2025, 2026, 2027]);
      }
    };
    loadYears();
  }, []);

  const loadDashboard = async () => {
    setLoading(true);
    try {
      const yearParam = selectedYear === 'all' ? null : selectedYear;
      const [resSummary, resProjects] = await Promise.all([
        dashboardAPI.getSummary(yearParam),
        projectsAPI.getAll()
      ]);
      setData(resSummary.data);
      setProjects(resProjects.data);
    } catch (err) {
      console.error('Failed to load dashboard data', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadDashboard();
    // Reload dashboard every 3 seconds to catch mode changes
    const interval = setInterval(loadDashboard, 3000);
    return () => clearInterval(interval);
  }, [selectedYear]);

  // Force chart re-render when theme changes (ECharts doesn't auto-detect)
  useEffect(() => {
    // This triggers re-render of all options with new isDark value
  }, [isDark]);

  const handleOpenEdit = (project) => {
    setSelectedProject(project);
    setModalOpen(true);
  };

  const handleCreateNew = () => {
    setSelectedProject({
      title: '',
      department: 'Quality',
      process_area: 'Slit Coater',
      category: 'Quality',
      priority: 'Medium',
      owner: '',
      start_date: new Date().toISOString().split('T')[0],
      due_date: new Date(Date.now() + 30*24*60*60*1000).toISOString().split('T')[0],
      status: 'Running',
      progress: 0,
      cost_saving: 0,
      horizontal_deploy: 'No'
    });
    setModalOpen(true);
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this CI project?')) {
      await projectsAPI.delete(id);
      loadDashboard();
      setModalOpen(false);
    }
  };

  const exportExcel = () => {
    const ws = XLSX.utils.json_to_sheet(projects);
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, 'CI Projects');
    XLSX.writeFile(wb, 'CIMS_CI_Projects_Master.xlsx');
  };

  if (loading || !data) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '60vh' }}>
        <CircularProgress size={50} />
      </Box>
    );
  }

  const { summary_cards, kpi_performance_table, project_status_distribution, project_category_distribution, monthly_kpi_trend } = data;

  // Chart options matching Image 3 Donut & Line charts
  const statusDonutOption = {
    tooltip: { trigger: 'item' },
    legend: { bottom: '2%', left: 'center', textStyle: { fontSize: 9, color: isDark ? '#cbd5e1' : '#000' }, itemWidth: 20 },
    color: ['#2E7D32', '#ED6C02', '#94a3b8'],
    series: [{
      name: 'Project Status',
      type: 'pie',
      center: ['50%', '40%'],
      radius: ['35%', '58%'],
      avoidLabelOverlap: true,
      label: { show: true, formatter: '{b}\n({d}%)', fontSize: 10, padding: 4, color: isDark ? '#e2e8f0' : '#000' },
      itemStyle: { borderColor: isDark ? '#1e293b' : '#fff', borderWidth: 2 },
      data: project_status_distribution
    }]
  };

  const categoryDonutOption = {
    tooltip: { trigger: 'item' },
    legend: { bottom: '2%', left: 'center', textStyle: { fontSize: 9, color: isDark ? '#cbd5e1' : '#000' }, itemWidth: 20 },
    color: ['#1565C0', '#2E7D32', '#ED6C02', '#8b5cf6', '#0288D1'],
    series: [{
      name: 'Project Category',
      type: 'pie',
      center: ['50%', '40%'],
      radius: ['35%', '58%'],
      avoidLabelOverlap: true,
      label: { show: true, formatter: '{d}%', fontSize: 10, padding: 4, color: isDark ? '#e2e8f0' : '#000' },
      itemStyle: { borderColor: isDark ? '#1e293b' : '#fff', borderWidth: 2 },
      data: project_category_distribution
    }]
  };
  const monthlyTrendOption = {
    tooltip: { trigger: 'axis', backgroundColor: isDark ? '#1e293b' : '#fff', textStyle: { color: isDark ? '#e2e8f0' : '#000' }, borderColor: isDark ? '#475569' : '#ccc' },
    legend: { top: '2%', textStyle: { color: isDark ? '#cbd5e1' : '#000', fontSize: 10 }, itemGap: 15, orient: 'horizontal' },
    grid: { left: '8%', right: '8%', bottom: '18%', top: '30%', containLabel: false },
    xAxis: { type: 'category', data: monthly_kpi_trend.months, axisLabel: { color: isDark ? '#94a3b8' : '#666', fontSize: 11, margin: 10 }, axisLine: { lineStyle: { color: isDark ? '#475569' : '#ccc' } } },
    yAxis: [
      { type: 'value', name: 'Rate (%)', nameTextStyle: { color: isDark ? '#94a3b8' : '#666', fontSize: 10 }, max: 100, axisLabel: { color: isDark ? '#94a3b8' : '#666', fontSize: 10 }, axisLine: { lineStyle: { color: isDark ? '#475569' : '#ccc' } }, splitLine: { lineStyle: { color: isDark ? '#334155' : '#e0e0e0' } } },
      { type: 'value', name: 'Days', nameTextStyle: { color: isDark ? '#94a3b8' : '#666', fontSize: 10 }, max: 60, axisLabel: { color: isDark ? '#94a3b8' : '#666', fontSize: 10 }, axisLine: { lineStyle: { color: isDark ? '#475569' : '#ccc' } }, splitLine: { lineStyle: { color: isDark ? '#334155' : '#e0e0e0' } } }
    ],
    series: [
      { name: 'On-time Completion Rate (%)', type: 'line', data: monthly_kpi_trend.on_time_rate, color: '#1565C0', lineStyle: { width: 2 }, itemStyle: { borderWidth: 0 }, smooth: true },
      { name: 'Effectiveness Rate (%)', type: 'line', data: monthly_kpi_trend.effectiveness_rate, color: '#2E7D32', lineStyle: { width: 2 }, itemStyle: { borderWidth: 0 }, smooth: true },
      { name: 'Avg Closing Time (Days)', type: 'line', yAxisIndex: 1, data: monthly_kpi_trend.avg_closing_time, color: '#8b5cf6', lineStyle: { width: 2 }, itemStyle: { borderWidth: 0 }, smooth: true }
    ]
  };

  return (
    <Box sx={{ p: 2 }}>
      {/* Top Banner Header matching Image 3 */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2, pb: 1, borderBottom: '2px solid #e2e8f0' }}>
        <Box>
          <Typography variant="h5" sx={{ fontWeight: 800, color: '#0F172A', letterSpacing: 0.5 }}>
            CONTINUAL IMPROVEMENT MASTER DASHBOARD
          </Typography>
          <Typography variant="caption" sx={{ color: '#64748b' }}>
            CI PROJECT MANAGEMENT & PERFORMANCE TRACKING | Date: 10.Jul.2026 | Version: 1.0
          </Typography>
        </Box>
        <Box sx={{ display: 'flex', gap: 1 }}>
          <Button variant="contained" color="primary" startIcon={<AddIcon />} onClick={handleCreateNew}>
            Add New CI Project
          </Button>
          <Button variant="outlined" startIcon={<ExportIcon />} onClick={exportExcel}>
            Export Excel
          </Button>
        </Box>
      </Box>

      {/* Row 1: Top 9 KPI Cards matching Image 3 */}
      <Grid container spacing={1.5} sx={{ mb: 2 }}>
        <Grid item xs={1.33}>
          <Card sx={{ textAlign: 'center', p: 1, backgroundColor: '#f8fafc', borderLeft: '4px solid #1565C0' }}>
            <Typography variant="caption" sx={{ fontWeight: 'bold', color: '#64748b' }}>TOTAL CI PROJECTS</Typography>
            <Typography variant="h5" sx={{ fontWeight: 800, my: 0.5 }}>{summary_cards.total.count}</Typography>
            <Chip label="100%" size="small" color="primary" sx={{ height: 18, fontSize: '0.65rem' }} />
          </Card>
        </Grid>
        <Grid item xs={1.33}>
          <Card sx={{ textAlign: 'center', p: 1, backgroundColor: '#f0fdf4', borderLeft: '4px solid #2E7D32' }}>
            <Typography variant="caption" sx={{ fontWeight: 'bold', color: '#166534' }}>COMPLETE</Typography>
            <Typography variant="h5" sx={{ fontWeight: 800, my: 0.5, color: '#2E7D32' }}>{summary_cards.complete.count}</Typography>
            <Chip label={`${summary_cards.complete.percent}%`} size="small" color="success" sx={{ height: 18, fontSize: '0.65rem' }} />
          </Card>
        </Grid>
        <Grid item xs={1.33}>
          <Card sx={{ textAlign: 'center', p: 1, backgroundColor: '#fff7ed', borderLeft: '4px solid #ED6C02' }}>
            <Typography variant="caption" sx={{ fontWeight: 'bold', color: '#9a3412' }}>RUNNING</Typography>
            <Typography variant="h5" sx={{ fontWeight: 800, my: 0.5, color: '#ED6C02' }}>{summary_cards.running.count}</Typography>
            <Chip label={`${summary_cards.running.percent}%`} size="small" color="warning" sx={{ height: 18, fontSize: '0.65rem' }} />
          </Card>
        </Grid>
        <Grid item xs={1.33}>
          <Card sx={{ textAlign: 'center', p: 1, backgroundColor: '#f1f5f9', borderLeft: '4px solid #64748b' }}>
            <Typography variant="caption" sx={{ fontWeight: 'bold', color: '#475569' }}>PENDING</Typography>
            <Typography variant="h5" sx={{ fontWeight: 800, my: 0.5, color: '#64748b' }}>{summary_cards.pending.count}</Typography>
            <Chip label={`${summary_cards.pending.percent}%`} size="small" sx={{ height: 18, fontSize: '0.65rem' }} />
          </Card>
        </Grid>
        <Grid item xs={1.33}>
          <Card sx={{ textAlign: 'center', p: 1, backgroundColor: '#f0f9ff', borderLeft: '4px solid #0288D1' }}>
            <Typography variant="caption" sx={{ fontWeight: 'bold', color: '#0369a1', fontSize: '0.65rem' }}>ON-TIME COMPLETION</Typography>
            <Typography variant="h5" sx={{ fontWeight: 800, my: 0.5, color: '#0288D1' }}>{summary_cards.on_time_rate.rate}%</Typography>
            <Typography variant="caption" sx={{ fontSize: '0.65rem', color: '#64748b' }}>Target ≥ {summary_cards.on_time_rate.target}%</Typography>
          </Card>
        </Grid>
        <Grid item xs={1.33}>
          <Card sx={{ textAlign: 'center', p: 1, backgroundColor: '#f0fdf4', borderLeft: '4px solid #2E7D32' }}>
            <Typography variant="caption" sx={{ fontWeight: 'bold', color: '#166534', fontSize: '0.65rem' }}>EFFECTIVENESS RATE</Typography>
            <Typography variant="h5" sx={{ fontWeight: 800, my: 0.5, color: '#2E7D32' }}>{summary_cards.effectiveness_rate.rate}%</Typography>
            <Typography variant="caption" sx={{ fontSize: '0.65rem', color: '#64748b' }}>Target ≥ {summary_cards.effectiveness_rate.target}%</Typography>
          </Card>
        </Grid>
        <Grid item xs={1.33}>
          <Card sx={{ textAlign: 'center', p: 1, backgroundColor: '#faf5ff', borderLeft: '4px solid #8b5cf6' }}>
            <Typography variant="caption" sx={{ fontWeight: 'bold', color: '#6b21a8', fontSize: '0.65rem' }}>AVG CLOSING TIME</Typography>
            <Typography variant="h5" sx={{ fontWeight: 800, my: 0.5, color: '#8b5cf6' }}>{summary_cards.avg_closing_days.days}</Typography>
            <Typography variant="caption" sx={{ fontSize: '0.65rem', color: '#64748b' }}>Days (Target &lt; {summary_cards.avg_closing_days.target})</Typography>
          </Card>
        </Grid>
        <Grid item xs={1.33}>
          <Card sx={{ textAlign: 'center', p: 1, backgroundColor: '#fefce8', borderLeft: '4px solid #ca8a04' }}>
            <Typography variant="caption" sx={{ fontWeight: 'bold', color: '#854d0e' }}>COST SAVING</Typography>
            <Typography variant="h6" sx={{ fontWeight: 800, my: 0.5, color: '#ca8a04', fontSize: '1.1rem' }}>${summary_cards.cost_saving.amount?.toLocaleString()}</Typography>
            <Typography variant="caption" sx={{ fontSize: '0.65rem', color: '#64748b' }}>Target ≥ ${summary_cards.cost_saving.target?.toLocaleString()}</Typography>
          </Card>
        </Grid>
        <Grid item xs={1.36}>
          <Card sx={{ textAlign: 'center', p: 1, backgroundColor: '#eff6ff', borderLeft: '4px solid #1d4ed8' }}>
            <Typography variant="caption" sx={{ fontWeight: 'bold', color: '#1e40af', fontSize: '0.65rem' }}>HORIZONTAL DEPLOY</Typography>
            <Typography variant="h5" sx={{ fontWeight: 800, my: 0.5, color: '#1d4ed8' }}>{summary_cards.horizontal_deployment.count}</Typography>
            <Typography variant="caption" sx={{ fontSize: '0.65rem', color: '#64748b' }}>Projects (Cases)</Typography>
          </Card>
        </Grid>
      </Grid>

      {/* Row 2: Sections 1, 2, 3, 4 matching Image 3 */}
      <Grid container spacing={1.5} sx={{ mb: 2 }}>
        {/* Section 1: KPI Performance Table */}
        <Grid item xs={3.2}>
          <Card sx={{ height: '260px' }}>
            <Box sx={{ backgroundColor: '#0F172A', color: '#fff', px: 1.5, py: 0.8 }}>
              <Typography variant="subtitle2" sx={{ fontWeight: 700, fontSize: '0.8rem' }}>1. KPI PERFORMANCE</Typography>
            </Box>
            <Box sx={{ overflowX: 'auto' }}>
              <Table size="small" sx={{ '& td, & th': { p: 0.6, fontSize: '0.72rem' } }}>
                <TableHead>
                  <TableRow>
                    <TableCell>KPI</TableCell>
                    <TableCell>Target</TableCell>
                    <TableCell>Actual</TableCell>
                    <TableCell>Status</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {kpi_performance_table.map((row) => (
                    <TableRow key={row.id}>
                      <TableCell sx={{ fontWeight: 'bold' }}>{row.id}. {row.name}</TableCell>
                      <TableCell>{row.target}</TableCell>
                      <TableCell sx={{ fontWeight: 'bold' }}>{row.actual}</TableCell>
                      <TableCell>
                        <Chip
                          label={row.status}
                          size="small"
                          color={row.status === 'Good' ? 'success' : (row.status === 'Close' ? 'warning' : 'error')}
                          sx={{ height: 18, fontSize: '0.65rem', fontWeight: 'bold' }}
                        />
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </Box>
          </Card>
        </Grid>

        {/* Section 2: Project Status Donut */}
        <Grid item xs={2.2}>
          <Card sx={{ height: '260px', backgroundColor: isDark ? '#1e293b' : '#fff' }}>
            <Box sx={{ backgroundColor: '#0F172A', color: '#fff', px: 1.5, py: 0.8 }}>
              <Typography variant="subtitle2" sx={{ fontWeight: 700, fontSize: '0.8rem' }}>2. PROJECT STATUS</Typography>
            </Box>
            <Box sx={{ height: '210px', p: 0.5, backgroundColor: isDark ? '#0f172a' : '#fff' }}>
              <ReactECharts option={statusDonutOption} style={{ height: '100%', width: '100%' }} />
            </Box>
          </Card>
        </Grid>

        {/* Section 3: Project Category Donut */}
        <Grid item xs={2.4}>
          <Card sx={{ height: '260px', backgroundColor: isDark ? '#1e293b' : '#fff' }}>
            <Box sx={{ backgroundColor: '#0F172A', color: '#fff', px: 1.5, py: 0.8 }}>
              <Typography variant="subtitle2" sx={{ fontWeight: 700, fontSize: '0.8rem' }}>3. PROJECT CATEGORY</Typography>
            </Box>
            <Box sx={{ height: '210px', p: 0.5, backgroundColor: isDark ? '#0f172a' : '#fff' }}>
              <ReactECharts option={categoryDonutOption} style={{ height: '100%', width: '100%' }} />
            </Box>
          </Card>
        </Grid>

        {/* Section 4: Monthly KPI Trend Chart */}
        <Grid item xs={4.2}>
          <Card sx={{ height: '260px', backgroundColor: isDark ? '#1e293b' : '#fff' }}>
            <Box sx={{ backgroundColor: '#0F172A', color: '#fff', px: 1.5, py: 0.8, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <Typography variant="subtitle2" sx={{ fontWeight: 700, fontSize: '0.8rem' }}>4. MONTHLY KPI TREND</Typography>
              <TextField
                select
                size="small"
                value={selectedYear}
                onChange={(e) => setSelectedYear(parseInt(e.target.value))}
                sx={{
                  width: '80px',
                  '& .MuiOutlinedInput-root': { backgroundColor: '#fff', height: '28px' },
                  '& .MuiOutlinedInput-input': { fontSize: '0.75rem', p: '4px 8px' }
                }}
              >
                <MenuItem value="all">All Years</MenuItem>
                {availableYears.map((y) => (
                  <MenuItem key={y} value={y}>{y}</MenuItem>
                ))}
              </TextField>
            </Box>
            <Box sx={{ height: '210px', p: 0.5, backgroundColor: isDark ? '#0f172a' : '#fff', overflow: 'hidden' }}>
              <ReactECharts option={monthlyTrendOption} style={{ height: '100%', width: '100%' }} />
            </Box>
          </Card>
        </Grid>
      </Grid>

      {/* Row 3: Section 5 CI Project Record Table matching Image 3 */}
      <Card sx={{ mb: 2 }}>
        <Box sx={{ backgroundColor: '#0F172A', color: '#fff', px: 2, py: 1, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <Typography variant="subtitle2" sx={{ fontWeight: 700 }}>5. CI PROJECT RECORD</Typography>
          <Typography variant="caption" sx={{ color: '#cbd5e1' }}>Click any CI No. to edit details & print reports</Typography>
        </Box>
        <Box sx={{ overflowX: 'auto' }}>
          <Table size="small" sx={{ minWidth: 1200, '& td, & th': { p: 0.8, fontSize: '0.75rem' } }}>
            <TableHead>
              <TableRow sx={{ backgroundColor: '#1E293B', '& td': { color: '#000000', fontWeight: 700 } }}>
                <TableCell sx={{ color: '#000000' }}>No.</TableCell>
                <TableCell sx={{ color: '#000000' }}>CI No.</TableCell>
                <TableCell sx={{ color: '#000000' }}>Project Title</TableCell>
                <TableCell sx={{ color: '#000000' }}>Category</TableCell>
                <TableCell sx={{ color: '#000000' }}>Process/Area</TableCell>
                <TableCell sx={{ color: '#000000' }}>Start Date</TableCell>
                <TableCell sx={{ color: '#000000' }}>Due Date</TableCell>
                <TableCell sx={{ color: '#000000' }}>Status</TableCell>
                <TableCell sx={{ color: '#000000' }}>Priority</TableCell>
                <TableCell sx={{ color: '#000000' }}>KPI / Target</TableCell>
                <TableCell sx={{ color: '#000000' }}>Before</TableCell>
                <TableCell sx={{ color: '#000000' }}>Target</TableCell>
                <TableCell sx={{ color: '#000000' }}>After</TableCell>
                <TableCell sx={{ color: '#000000' }}>Ach (%)</TableCell>
                <TableCell sx={{ color: '#000000' }}>Result</TableCell>
                <TableCell sx={{ color: '#000000' }}>Verified</TableCell>
                <TableCell sx={{ color: '#000000' }}>Cost Saving ($)</TableCell>
                <TableCell sx={{ color: '#000000' }}>Yokoten</TableCell>
                <TableCell sx={{ color: '#000000' }}>Close Date</TableCell>
                <TableCell sx={{ color: '#000000' }}>Action</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {projects.slice(0, 10).map((p, idx) => (
                <TableRow key={p.id} hover sx={{ '&:nth-of-type(odd)': { backgroundColor: '#f8fafc' } }}>
                  <TableCell>{idx + 1}</TableCell>
                  <TableCell>
                    <Typography
                      variant="caption"
                      sx={{ fontWeight: 'bold', color: '#1565C0', cursor: 'pointer', textDecoration: 'underline' }}
                      onClick={() => handleOpenEdit(p)}
                    >
                      {p.ci_no}
                    </Typography>
                  </TableCell>
                  <TableCell sx={{ fontWeight: 600 }}>{p.title}</TableCell>
                  <TableCell>{p.category}</TableCell>
                  <TableCell>{p.process_area}</TableCell>
                  <TableCell>{p.start_date}</TableCell>
                  <TableCell>{p.due_date}</TableCell>
                  <TableCell>
                    <Chip
                      label={p.status}
                      size="small"
                      color={p.status === 'Complete' ? 'success' : (p.status === 'Running' ? 'warning' : 'default')}
                      sx={{ height: 20, fontSize: '0.65rem', fontWeight: 'bold' }}
                    />
                  </TableCell>
                  <TableCell>
                    <Chip
                      label={p.priority}
                      size="small"
                      variant="outlined"
                      color={p.priority === 'High' ? 'error' : (p.priority === 'Medium' ? 'warning' : 'success')}
                      sx={{ height: 20, fontSize: '0.65rem' }}
                    />
                  </TableCell>
                  <TableCell>{p.kpi_metric || '-'}</TableCell>
                  <TableCell>{p.before_value ?? '-'}</TableCell>
                  <TableCell>{p.target_value ?? '-'}</TableCell>
                  <TableCell>{p.after_value ?? '-'}</TableCell>
                  <TableCell sx={{ fontWeight: 'bold' }}>{p.achievement_rate ? `${p.achievement_rate}%` : '-'}</TableCell>
                  <TableCell>
                    {p.result === 'PASS' && <Chip label="PASS" size="small" color="success" sx={{ height: 18, fontSize: '0.6rem' }} />}
                    {p.result === 'FAIL' && <Chip label="FAIL" size="small" color="error" sx={{ height: 18, fontSize: '0.6rem' }} />}
                    {(!p.result || p.result === '-') && '-'}
                  </TableCell>
                  <TableCell>{p.verified}</TableCell>
                  <TableCell sx={{ fontWeight: 'bold' }}>${p.cost_saving?.toLocaleString()}</TableCell>
                  <TableCell>{p.horizontal_deploy}</TableCell>
                  <TableCell>{p.close_date || '-'}</TableCell>
                  <TableCell>
                    <IconButton size="small" color="primary" onClick={() => handleOpenEdit(p)}>
                      <EditIcon fontSize="inherit" />
                    </IconButton>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </Box>
      </Card>

      {/* Row 4: Sections 6, 7, 8 matching Image 3 */}
      <Grid container spacing={1.5}>
        <Grid item xs={4.5}>
          <Card sx={{ height: '140px', p: 1.5 }}>
            <Typography variant="caption" sx={{ fontWeight: 'bold', color: '#1565C0', display: 'block', mb: 1 }}>
              6. CI PROCESS FLOW (PDCA & DMAIC)
            </Typography>
            <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', pt: 1 }}>
              {['Problem ID', 'Root Cause', 'Countermeasure', 'Implement', 'Verify', 'Yokoten', 'Closed'].map((step, i) => (
                <React.Fragment key={step}>
                  <Box sx={{ textAlign: 'center' }}>
                    <Box sx={{ width: 24, height: 24, borderRadius: '50%', backgroundColor: '#1565C0', color: '#fff', fontSize: '0.7rem', display: 'flex', alignItems: 'center', justifyContent: 'center', mx: 'auto', fontWeight: 'bold' }}>
                      {i + 1}
                    </Box>
                    <Typography variant="caption" sx={{ fontSize: '0.6rem', fontWeight: 600, display: 'block', mt: 0.5 }}>{step}</Typography>
                  </Box>
                  {i < 6 && <Typography variant="caption" sx={{ color: '#94a3b8' }}>→</Typography>}
                </React.Fragment>
              ))}
            </Box>
          </Card>
        </Grid>

        <Grid item xs={4.5}>
          <Card sx={{ height: '140px', p: 1.5 }}>
            <Typography variant="caption" sx={{ fontWeight: 'bold', color: '#1565C0', display: 'block', mb: 0.5 }}>
              7. KPI FORMULA
            </Typography>
            <Typography variant="caption" sx={{ display: 'block', fontSize: '0.65rem', color: '#334155' }}>
              • <strong>On-time Completion Rate (%)</strong> = (Completed Projects on Time ÷ Total Completed) × 100%<br />
              • <strong>Effectiveness Rate (%)</strong> = (Verified PASS Projects ÷ Total Completed) × 100%<br />
              • <strong>Average Closing Time (Days)</strong> = Σ Closing Days of Completed Projects ÷ Total Completed
            </Typography>
          </Card>
        </Grid>

        <Grid item xs={3}>
          <Card sx={{ height: '140px', p: 1.5 }}>
            <Typography variant="caption" sx={{ fontWeight: 'bold', color: '#1565C0', display: 'block', mb: 0.5 }}>
              8. NOTES & LEGEND
            </Typography>
            <Typography variant="caption" sx={{ display: 'block', fontSize: '0.65rem', color: '#475569', mb: 0.5 }}>
              • KPI calculated on completed projects only.<br />
              • Horizontal Deployment = Applied to other lines/areas.
            </Typography>
            <Box sx={{ display: 'flex', gap: 1 }}>
              <Chip label="Complete" color="success" size="small" sx={{ height: 16, fontSize: '0.6rem' }} />
              <Chip label="Running" color="warning" size="small" sx={{ height: 16, fontSize: '0.6rem' }} />
              <Chip label="Pending" size="small" sx={{ height: 16, fontSize: '0.6rem' }} />
            </Box>
          </Card>
        </Grid>
      </Grid>

      {/* Pop-up Edit Modal */}
      <CIEditModal
        open={modalOpen}
        onClose={() => setModalOpen(false)}
        project={selectedProject}
        onSaved={loadDashboard}
        onDelete={handleDelete}
      />
    </Box>
  );
}
