import React, { useState, useEffect } from 'react';
import {
  Box, Card, CardContent, Typography, Table, TableHead, TableRow, TableCell, TableBody,
  Button, TextField, MenuItem, Chip, IconButton, InputAdornment, Grid
} from '@mui/material';
import {
  Search as SearchIcon, Add as AddIcon, Edit as EditIcon, Delete as DeleteIcon,
  FileDownload as ExportIcon, Print as PrintIcon
} from '@mui/icons-material';
import { projectsAPI } from '../services/api';
import CIEditModal from '../components/CIEditModal';
import * as XLSX from 'xlsx';

export default function ProjectRegister() {
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [category, setCategory] = useState('All');
  const [department, setDepartment] = useState('All');
  const [statusFilter, setStatusFilter] = useState('All');
  
  const [selectedProject, setSelectedProject] = useState(null);
  const [modalOpen, setModalOpen] = useState(false);

  const fetchProjects = async () => {
    setLoading(true);
    try {
      const res = await projectsAPI.getAll({
        search: search || undefined,
        category: category !== 'All' ? category : undefined,
        department: department !== 'All' ? department : undefined,
        status: statusFilter !== 'All' ? statusFilter : undefined,
      });
      setProjects(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProjects();
  }, [search, category, department, statusFilter]);

  const handleOpenEdit = (p) => {
    setSelectedProject(p);
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
      fetchProjects();
      setModalOpen(false);
    }
  };

  const exportExcel = () => {
    const ws = XLSX.utils.json_to_sheet(projects);
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, 'CI_Register');
    XLSX.writeFile(wb, 'CIMS_CI_Project_Register.xlsx');
  };

  return (
    <Box sx={{ p: 3 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Box>
          <Typography variant="h5" sx={{ fontWeight: 800 }}>CI Project Register</Typography>
          <Typography variant="body2" sx={{ color: '#64748b' }}>Centralized Continuous Improvement Project Repository</Typography>
        </Box>
        <Box sx={{ display: 'flex', gap: 1.5 }}>
          <Button variant="contained" color="primary" startIcon={<AddIcon />} onClick={handleCreateNew}>
            Add New Project
          </Button>
          <Button variant="outlined" startIcon={<ExportIcon />} onClick={exportExcel}>
            Export Excel
          </Button>
        </Box>
      </Box>

      {/* Search & Filters */}
      <Card sx={{ mb: 3, p: 2 }}>
        <Grid container spacing={2} alignItems="center">
          <Grid item xs={3.5}>
            <TextField
              size="small"
              fullWidth
              placeholder="Search by CI No, Title, Leader..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              InputProps={{
                startAdornment: <InputAdornment position="start"><SearchIcon /></InputAdornment>
              }}
            />
          </Grid>
          <Grid item xs={2.5}>
            <TextField select size="small" fullWidth label="Category" value={category} onChange={(e) => setCategory(e.target.value)}>
              {['All', 'Quality', 'Productivity', 'Cost Saving', 'Equipment', 'Safety / Environment', 'Others'].map((c) => (
                <MenuItem key={c} value={c}>{c}</MenuItem>
              ))}
            </TextField>
          </Grid>
          <Grid item xs={2.5}>
            <TextField select size="small" fullWidth label="Department" value={department} onChange={(e) => setDepartment(e.target.value)}>
              {['All', 'Quality', 'Production', 'TPM', 'Slit Coater', 'Wet Bench', 'IOX', 'Overall'].map((d) => (
                <MenuItem key={d} value={d}>{d}</MenuItem>
              ))}
            </TextField>
          </Grid>
          <Grid item xs={2.5}>
            <TextField select size="small" fullWidth label="Status" value={statusFilter} onChange={(e) => setStatusFilter(e.target.value)}>
              {['All', 'Complete', 'Running', 'Pending'].map((s) => (
                <MenuItem key={s} value={s}>{s}</MenuItem>
              ))}
            </TextField>
          </Grid>
        </Grid>
      </Card>

      {/* Main Table */}
      <Card>
        <Box sx={{ overflowX: 'auto' }}>
          <Table size="small" sx={{ minWidth: 1100 }}>
            <TableHead>
              <TableRow sx={{ backgroundColor: '#1E293B', '& td': { color: '#000000', fontWeight: 700 } }}>
                <TableCell>CI No.</TableCell>
                <TableCell>Project Title</TableCell>
                <TableCell>Category</TableCell>
                <TableCell>Department</TableCell>
                <TableCell>Leader</TableCell>
                <TableCell>Start</TableCell>
                <TableCell>Due</TableCell>
                <TableCell>Status</TableCell>
                <TableCell>Priority</TableCell>
                <TableCell>Ach (%)</TableCell>
                <TableCell>QA Verified</TableCell>
                <TableCell>Cost Saving ($)</TableCell>
                <TableCell>Actions</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {projects.map((p) => (
                <TableRow key={p.id} hover>
                  <TableCell sx={{ fontWeight: 'bold', color: '#1565C0', cursor: 'pointer' }} onClick={() => handleOpenEdit(p)}>
                    {p.ci_no}
                  </TableCell>
                  <TableCell sx={{ fontWeight: 600 }}>{p.title}</TableCell>
                  <TableCell>{p.category}</TableCell>
                  <TableCell>{p.department}</TableCell>
                  <TableCell>{p.owner}</TableCell>
                  <TableCell>{p.start_date}</TableCell>
                  <TableCell>{p.due_date}</TableCell>
                  <TableCell>
                    <Chip label={p.status} size="small" color={p.status === 'Complete' ? 'success' : (p.status === 'Running' ? 'warning' : 'default')} sx={{ height: 20, fontSize: '0.7rem', fontWeight: 'bold' }} />
                  </TableCell>
                  <TableCell>
                    <Chip label={p.priority} size="small" variant="outlined" color={p.priority === 'High' ? 'error' : 'warning'} sx={{ height: 20, fontSize: '0.7rem' }} />
                  </TableCell>
                  <TableCell sx={{ fontWeight: 'bold' }}>{p.achievement_rate ? `${p.achievement_rate}%` : '-'}</TableCell>
                  <TableCell>{p.verified}</TableCell>
                  <TableCell sx={{ fontWeight: 'bold' }}>${p.cost_saving?.toLocaleString()}</TableCell>
                  <TableCell>
                    <IconButton size="small" color="primary" onClick={() => handleOpenEdit(p)}>
                      <EditIcon fontSize="inherit" />
                    </IconButton>
                    <IconButton size="small" color="error" onClick={() => handleDelete(p.id)}>
                      <DeleteIcon fontSize="inherit" />
                    </IconButton>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </Box>
      </Card>

      <CIEditModal
        open={modalOpen}
        onClose={() => setModalOpen(false)}
        project={selectedProject}
        onSaved={fetchProjects}
        onDelete={handleDelete}
      />
    </Box>
  );
}
