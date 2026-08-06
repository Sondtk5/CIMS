import React from 'react';
import { Box, Typography, Table, TableBody, TableCell, TableRow, Grid } from '@mui/material';

export default function CIReportPrintView({ project }) {
  if (!project) return null;

  const fiveWhyList = project.analyze_stage?.five_why || [
    { why: 'Why 1: Problem observed?', answer: project.issue_description || 'Defect occurring in process' },
    { why: 'Why 2: Direct cause?', answer: 'Equipment component wear / misalignment' },
    { why: 'Why 3: Root mechanism?', answer: 'Lack of calibration checklist' },
    { why: 'Why 4: Systemic cause?', answer: 'Maintenance PM interval exceeded' },
    { why: 'Why 5: Root Cause?', answer: 'Standard operating procedure missing PM audit rule' }
  ];

  return (
    <Box className="printable-area" sx={{ p: 3, backgroundColor: '#fff', color: '#000', fontFamily: 'Arial, sans-serif', maxWidth: '900px', margin: '0 auto', border: '1px solid #ccc' }}>
      {/* Header matching Image 2 */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderBottom: '3px solid #0F172A', pb: 1, mb: 2 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <Box sx={{ border: '2px solid #1565C0', p: 0.5, fontWeight: 900, color: '#1565C0', fontSize: '1.2rem', lineHeight: 1 }}>
            UTI
          </Box>
          <Typography variant="caption" sx={{ fontWeight: 'bold' }}>Unique Technology Integral</Typography>
        </Box>
        <Box sx={{ textAlign: 'center' }}>
          <Typography variant="h5" sx={{ fontWeight: 800, color: '#0F172A', letterSpacing: 1 }}>CI PROJECT REPORT</Typography>
          <Typography variant="subtitle1" sx={{ fontWeight: 700, color: '#475569' }}>CI 프로젝트 보고서</Typography>
        </Box>
        <Box sx={{ fontSize: '0.75rem' }}>
          <Table size="small" sx={{ borderCollapse: 'collapse', '& td': { border: '1px solid #000', p: 0.4 } }}>
            <TableBody>
              <TableRow><TableCell sx={{ fontWeight: 'bold' }}>From No.</TableCell><TableCell>{project.start_date}</TableCell></TableRow>
              <TableRow><TableCell sx={{ fontWeight: 'bold' }}>Revision</TableCell><TableCell>1.0</TableCell></TableRow>
              <TableRow><TableCell sx={{ fontWeight: 'bold' }}>Effective</TableCell><TableCell>2026-07-01</TableCell></TableRow>
            </TableBody>
          </Table>
        </Box>
      </Box>

      {/* Project Meta Info */}
      <Table size="small" sx={{ mb: 2, '& td': { border: '1px solid #cbd5e1', p: 0.6, fontSize: '0.8rem' } }}>
        <TableBody>
          <TableRow>
            <TableCell sx={{ fontWeight: 'bold', width: '15%', backgroundColor: '#f8fafc' }}>CI No.</TableCell>
            <TableCell sx={{ width: '35%', fontWeight: 'bold', color: '#1565C0' }}>{project.ci_no}</TableCell>
            <TableCell sx={{ fontWeight: 'bold', width: '15%', backgroundColor: '#f8fafc' }}>Project Title</TableCell>
            <TableCell sx={{ width: '35%', fontWeight: 'bold' }}>{project.title}</TableCell>
          </TableRow>
          <TableRow>
            <TableCell sx={{ fontWeight: 'bold', backgroundColor: '#f8fafc' }}>Department</TableCell>
            <TableCell>{project.department} ({project.process_area})</TableCell>
            <TableCell sx={{ fontWeight: 'bold', backgroundColor: '#f8fafc' }}>Project Leader</TableCell>
            <TableCell>{project.owner}</TableCell>
          </TableRow>
          <TableRow>
            <TableCell sx={{ fontWeight: 'bold', backgroundColor: '#f8fafc' }}>Start Date</TableCell>
            <TableCell>{project.start_date}</TableCell>
            <TableCell sx={{ fontWeight: 'bold', backgroundColor: '#f8fafc' }}>Target Due Date</TableCell>
            <TableCell>{project.due_date}</TableCell>
          </TableRow>
        </TableBody>
      </Table>

      {/* DMAIC 5-Stage Columns matching Image 2 */}
      <Grid container spacing={1} sx={{ mb: 2 }}>
        {/* DEFINE */}
        <Grid item xs={2.4}>
          <Box sx={{ border: '1px solid #84cc16', borderRadius: 1, overflow: 'hidden' }}>
            <Box sx={{ backgroundColor: '#84cc16', color: '#fff', textAlign: 'center', p: 0.5, fontWeight: 'bold', fontSize: '0.8rem' }}>
              1. DEFINE
            </Box>
            <Box sx={{ p: 1, fontSize: '0.75rem', minHeight: '140px' }}>
              <Typography variant="caption" sx={{ fontWeight: 'bold', display: 'block', color: '#4d7c0f' }}>Project Definition</Typography>
              • {project.title}<br />
              <Typography variant="caption" sx={{ fontWeight: 'bold', display: 'block', mt: 0.5, color: '#4d7c0f' }}>Problem Description</Typography>
              • {project.issue_description || 'Quality defect optimization'}<br />
              <Typography variant="caption" sx={{ fontWeight: 'bold', display: 'block', mt: 0.5, color: '#4d7c0f' }}>Target Metric</Typography>
              • {project.kpi_metric}: {project.target_value}
            </Box>
          </Box>
        </Grid>

        {/* MEASURE */}
        <Grid item xs={2.4}>
          <Box sx={{ border: '1px solid #10b981', borderRadius: 1, overflow: 'hidden' }}>
            <Box sx={{ backgroundColor: '#10b981', color: '#fff', textAlign: 'center', p: 0.5, fontWeight: 'bold', fontSize: '0.8rem' }}>
              2. MEASURE
            </Box>
            <Box sx={{ p: 1, fontSize: '0.75rem', minHeight: '140px' }}>
              <Typography variant="caption" sx={{ fontWeight: 'bold', display: 'block', color: '#047857' }}>Measure Current Status</Typography>
              • Baseline: {project.before_value} {project.kpi_metric}<br />
              <Typography variant="caption" sx={{ fontWeight: 'bold', display: 'block', mt: 0.5, color: '#047857' }}>Data Collection</Typography>
              • Process: {project.process_area}<br />
              • Sample Size: 100 Lots
            </Box>
          </Box>
        </Grid>

        {/* ANALYZE */}
        <Grid item xs={2.4}>
          <Box sx={{ border: '1px solid #14b8a6', borderRadius: 1, overflow: 'hidden' }}>
            <Box sx={{ backgroundColor: '#14b8a6', color: '#fff', textAlign: 'center', p: 0.5, fontWeight: 'bold', fontSize: '0.8rem' }}>
              3. ANALYZE
            </Box>
            <Box sx={{ p: 1, fontSize: '0.75rem', minHeight: '140px' }}>
              <Typography variant="caption" sx={{ fontWeight: 'bold', display: 'block', color: '#0f766e' }}>Root Cause Analysis</Typography>
              • 5-Why RCA Performed<br />
              • Fishbone (4M1E)<br />
              <Typography variant="caption" sx={{ fontWeight: 'bold', display: 'block', mt: 0.5, color: '#0f766e' }}>Root Cause</Typography>
              • {fiveWhyList[fiveWhyList.length - 1]?.answer || 'Subsystem drift'}
            </Box>
          </Box>
        </Grid>

        {/* IMPROVE */}
        <Grid item xs={2.4}>
          <Box sx={{ border: '1px solid #3b82f6', borderRadius: 1, overflow: 'hidden' }}>
            <Box sx={{ backgroundColor: '#3b82f6', color: '#fff', textAlign: 'center', p: 0.5, fontWeight: 'bold', fontSize: '0.8rem' }}>
              4. IMPROVE
            </Box>
            <Box sx={{ p: 1, fontSize: '0.75rem', minHeight: '140px' }}>
              <Typography variant="caption" sx={{ fontWeight: 'bold', display: 'block', color: '#1d4ed8' }}>Improvement Action</Typography>
              • Countermeasure implemented<br />
              • Pilot Test Completed<br />
              • Resource Allocated
            </Box>
          </Box>
        </Grid>

        {/* CONTROL */}
        <Grid item xs={2.4}>
          <Box sx={{ border: '1px solid #8b5cf6', borderRadius: 1, overflow: 'hidden' }}>
            <Box sx={{ backgroundColor: '#8b5cf6', color: '#fff', textAlign: 'center', p: 0.5, fontWeight: 'bold', fontSize: '0.8rem' }}>
              5. CONTROL
            </Box>
            <Box sx={{ p: 1, fontSize: '0.75rem', minHeight: '140px' }}>
              <Typography variant="caption" sx={{ fontWeight: 'bold', display: 'block', color: '#6d28d9' }}>Control & Standardize</Typography>
              • SOP / WI Revised<br />
              • Training Completed<br />
              • Yokoten: {project.horizontal_deploy}
            </Box>
          </Box>
        </Grid>
      </Grid>

      {/* Bottom 3 Boxes: Verification, Benefit/Saving, Lessons Learned */}
      <Grid container spacing={1} sx={{ mb: 2 }}>
        <Grid item xs={4}>
          <Box sx={{ border: '1px solid #93c5fd', borderRadius: 1, p: 1, minHeight: '120px' }}>
            <Typography variant="caption" sx={{ fontWeight: 'bold', color: '#1d4ed8', borderBottom: '1px solid #93c5fd', display: 'block', pb: 0.5, mb: 0.5 }}>
              Verification (검증)
            </Typography>
            <Typography variant="caption" sx={{ display: 'block', fontSize: '0.75rem' }}>
              • Before Data: {project.before_value}<br />
              • Target: {project.target_value}<br />
              • After Data: {project.after_value}<br />
              • Achievement: <strong>{project.achievement_rate}%</strong><br />
              • Result: <span style={{ color: project.result === 'PASS' ? 'green' : 'red', fontWeight: 'bold' }}>{project.result}</span>
            </Typography>
          </Box>
        </Grid>

        <Grid item xs={4}>
          <Box sx={{ border: '1px solid #93c5fd', borderRadius: 1, p: 1, minHeight: '120px' }}>
            <Typography variant="caption" sx={{ fontWeight: 'bold', color: '#1d4ed8', borderBottom: '1px solid #93c5fd', display: 'block', pb: 0.5, mb: 0.5 }}>
              Benefit / Saving (효과/절감액)
            </Typography>
            <Typography variant="caption" sx={{ display: 'block', fontSize: '0.75rem' }}>
              • Category: {project.category}<br />
              • Saving Amount: <strong>${project.cost_saving?.toLocaleString()}</strong> / year<br />
              • Non-financial: Productivity & Quality Improvement
            </Typography>
          </Box>
        </Grid>

        <Grid item xs={4}>
          <Box sx={{ border: '1px solid #93c5fd', borderRadius: 1, p: 1, minHeight: '120px' }}>
            <Typography variant="caption" sx={{ fontWeight: 'bold', color: '#1d4ed8', borderBottom: '1px solid #93c5fd', display: 'block', pb: 0.5, mb: 0.5 }}>
              Lessons Learned (교훈)
            </Typography>
            <Typography variant="caption" sx={{ display: 'block', fontSize: '0.75rem' }}>
              • Standardized PM checklist prevents recurring defects.<br />
              • Yokoten deployment to other process lines.
            </Typography>
          </Box>
        </Grid>
      </Grid>

      {/* Approval Signatures */}
      <Table size="small" sx={{ '& td': { border: '1px solid #000', p: 0.5, textAlign: 'center', fontSize: '0.75rem' } }}>
        <TableBody>
          <TableRow sx={{ backgroundColor: '#f1f5f9' }}>
            <TableCell sx={{ fontWeight: 'bold', width: '33%' }}>Prepared By (작성)</TableCell>
            <TableCell sx={{ fontWeight: 'bold', width: '33%' }}>Reviewed By (검토)</TableCell>
            <TableCell sx={{ fontWeight: 'bold', width: '34%' }}>Approved By (승인)</TableCell>
          </TableRow>
          <TableRow sx={{ height: '90px', verticalAlign: 'bottom' }}>
            <TableCell sx={{ verticalAlign: 'bottom' }}>{project.owner}</TableCell>
            <TableCell sx={{ verticalAlign: 'bottom' }}>{project.tpm_reviewed_by || ''}</TableCell>
            <TableCell sx={{ verticalAlign: 'bottom' }}>{project.tpm_decision === 'Approved' && project.tpm_approved_by ? project.tpm_approved_by : ''}</TableCell>
          </TableRow>
          <TableRow sx={{ height: '45px' }}>
            <TableCell>Date: {project.start_date}</TableCell>
            <TableCell>{project.tpm_review_date ? `Date: ${project.tpm_review_date}` : ''}</TableCell>
            <TableCell>{project.tpm_decision === 'Approved' && project.tpm_approve_date ? `Date: ${project.tpm_approve_date}` : ''}</TableCell>
          </TableRow>
        </TableBody>
      </Table>
    </Box>
  );
}
