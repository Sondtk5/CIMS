import React, { useState, useEffect } from 'react';
import { Box, Card, CardContent, Typography, Table, TableHead, TableRow, TableCell, TableBody, Chip } from '@mui/material';
import { History as HistoryIcon } from '@mui/icons-material';
import { auditAPI } from '../services/api';

export default function AuditLogs() {
  const [logs, setLogs] = useState([]);

  useEffect(() => {
    auditAPI.getLogs().then((res) => setLogs(res.data)).catch(console.error);
  }, []);

  return (
    <Box sx={{ p: 3 }}>
      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1.5, mb: 3 }}>
        <HistoryIcon color="primary" sx={{ fontSize: 32 }} />
        <Box>
          <Typography variant="h5" sx={{ fontWeight: 800 }}>ISO 9001 / Log Tracking</Typography>
          <Typography variant="body2" sx={{ color: '#64748b' }}>Immutable record of all project modifications, verifications, and approvals</Typography>
        </Box>
      </Box>

      <Card>
        <CardContent>
          <Table size="small">
            <TableHead>
              <TableRow sx={{ backgroundColor: '#f1f5f9' }}>
                <TableCell sx={{ fontWeight: 'bold' }}>Timestamp</TableCell>
                <TableCell sx={{ fontWeight: 'bold' }}>User</TableCell>
                <TableCell sx={{ fontWeight: 'bold' }}>Role</TableCell>
                <TableCell sx={{ fontWeight: 'bold' }}>Action</TableCell>
                <TableCell sx={{ fontWeight: 'bold' }}>CI No.</TableCell>
                <TableCell sx={{ fontWeight: 'bold' }}>Details / Reason</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {logs.map((log) => (
                <TableRow key={log.id} hover>
                  <TableCell sx={{ fontSize: '0.8rem', color: '#64748b' }}>
                    {new Date(log.timestamp).toLocaleString()}
                  </TableCell>
                  <TableCell sx={{ fontWeight: 600 }}>{log.user_name}</TableCell>
                  <TableCell>
                    <Chip label={log.user_role} size="small" variant="outlined" sx={{ height: 20, fontSize: '0.65rem' }} />
                  </TableCell>
                  <TableCell>
                    <Chip
                      label={log.action_type}
                      size="small"
                      color={log.action_type === 'CREATE' ? 'success' : (log.action_type === 'DELETE' ? 'error' : 'info')}
                      sx={{ height: 20, fontSize: '0.65rem', fontWeight: 'bold' }}
                    />
                  </TableCell>
                  <TableCell sx={{ fontWeight: 'bold', color: '#1565C0' }}>{log.ci_no || '-'}</TableCell>
                  <TableCell sx={{ fontSize: '0.85rem' }}>{log.reason || log.field_changed}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </Box>
  );
}
