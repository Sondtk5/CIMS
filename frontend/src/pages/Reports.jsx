import React, { useState, useEffect } from 'react';
import {
  Box, Card, CardContent, Typography, Grid, Table, TableHead, TableRow, TableCell, TableBody, Button, Chip
} from '@mui/material';
import { Assessment as ReportIcon, FileDownload as ExportIcon, Print as PrintIcon } from '@mui/icons-material';
import { reportsAPI } from '../services/api';
import * as XLSX from 'xlsx';

export default function Reports() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    reportsAPI.getSummary()
      .then((res) => setData(res.data))
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  if (loading || !data) return null;

  const exportExcel = () => {
    const ws = XLSX.utils.json_to_sheet(data.department_summary);
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, 'Department_Summary');
    XLSX.writeFile(wb, 'CIMS_Department_CI_Report.xlsx');
  };

  return (
    <Box sx={{ p: 3 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1.5 }}>
          <ReportIcon color="primary" sx={{ fontSize: 32 }} />
          <Box>
            <Typography variant="h5" sx={{ fontWeight: 800 }}>CI Reports & Summary</Typography>
            <Typography variant="body2" sx={{ color: '#64748b' }}>Executive and Departmental Performance Summaries</Typography>
          </Box>
        </Box>
        <Box sx={{ display: 'flex', gap: 1 }}>
          <Button variant="contained" color="primary" startIcon={<ExportIcon />} onClick={exportExcel}>
            Export Excel Report
          </Button>
          <Button variant="outlined" startIcon={<PrintIcon />} onClick={() => window.print()}>
            Print Report
          </Button>
        </Box>
      </Box>

      {/* Department Summary */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Typography variant="h6" sx={{ fontWeight: 700, mb: 2 }}>Departmental Performance Breakdown</Typography>
          <Table size="small">
            <TableHead>
              <TableRow sx={{ backgroundColor: '#f1f5f9' }}>
                <TableCell sx={{ fontWeight: 'bold' }}>Department / Line</TableCell>
                <TableCell sx={{ fontWeight: 'bold' }}>Total CI Projects</TableCell>
                <TableCell sx={{ fontWeight: 'bold' }}>Completed</TableCell>
                <TableCell sx={{ fontWeight: 'bold' }}>Completion Rate (%)</TableCell>
                <TableCell sx={{ fontWeight: 'bold' }}>Total Cost Savings ($)</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {data.department_summary.map((row) => (
                <TableRow key={row.department} hover>
                  <TableCell sx={{ fontWeight: 600 }}>{row.department}</TableCell>
                  <TableCell>{row.total_projects}</TableCell>
                  <TableCell>{row.completed}</TableCell>
                  <TableCell sx={{ fontWeight: 'bold' }}>{row.completion_rate}%</TableCell>
                  <TableCell sx={{ fontWeight: 'bold', color: '#1565C0' }}>${row.cost_saving?.toLocaleString()}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </Box>
  );
}
