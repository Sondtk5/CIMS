import React from 'react';
import { Box, Typography, Table, TableBody, TableCell, TableRow, Chip } from '@mui/material';

export default function CIRequestFormPrintView({ project }) {
  if (!project) return null;

  return (
    <Box className="printable-area" sx={{ p: 3, backgroundColor: '#fff', color: '#000', fontFamily: 'Arial, sans-serif', maxWidth: '800px', margin: '0 auto', border: '1px solid #ccc' }}>
      {/* Header matching Image 1 */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderBottom: '3px solid #0F172A', pb: 1, mb: 2 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <Box sx={{ border: '2px solid #1565C0', p: 0.5, fontWeight: 900, color: '#1565C0', fontSize: '1.2rem', lineHeight: 1 }}>
            UTI
          </Box>
          <Box>
            <Typography variant="subtitle2" sx={{ fontWeight: 'bold', fontSize: '0.75rem' }}>Unique Technology Integral</Typography>
          </Box>
        </Box>
        <Box sx={{ textAlign: 'center' }}>
          <Typography variant="h5" sx={{ fontWeight: 800, color: '#0F172A', letterSpacing: 1 }}>CI REQUEST FORM</Typography>
          <Typography variant="subtitle1" sx={{ fontWeight: 700, color: '#475569' }}>CI 요청서</Typography>
        </Box>
        <Box sx={{ border: '1px solid #000', fontSize: '0.75rem' }}>
          <Table size="small" sx={{ borderCollapse: 'collapse', '& td': { border: '1px solid #000', p: 0.5 } }}>
            <TableBody>
              <TableRow><TableCell sx={{ fontWeight: 'bold' }}>From No.</TableCell><TableCell>{project.start_date || 'yyyy-mm-dd'}</TableCell></TableRow>
              <TableRow><TableCell sx={{ fontWeight: 'bold' }}>Revision</TableCell><TableCell>1.0</TableCell></TableRow>
              <TableRow><TableCell sx={{ fontWeight: 'bold' }}>Effective</TableCell><TableCell>2026-07-01</TableCell></TableRow>
            </TableBody>
          </Table>
        </Box>
      </Box>

      {/* A. GENERAL INFORMATION */}
      <Typography variant="subtitle2" sx={{ fontWeight: 'bold', backgroundColor: '#e2e8f0', p: 0.5, mb: 1 }}>
        A. GENERAL INFORMATION (일반 정보)
      </Typography>
      <Table size="small" sx={{ mb: 2, '& td': { border: '1px solid #cbd5e1', p: 0.8, fontSize: '0.85rem' } }}>
        <TableBody>
          <TableRow>
            <TableCell sx={{ fontWeight: 'bold', width: '20%', backgroundColor: '#f8fafc' }}>CI No.</TableCell>
            <TableCell sx={{ width: '30%', fontWeight: 'bold', color: '#1565C0' }}>{project.ci_no}</TableCell>
            <TableCell sx={{ fontWeight: 'bold', width: '20%', backgroundColor: '#f8fafc' }}>Request Date</TableCell>
            <TableCell sx={{ width: '30%' }}>{project.start_date}</TableCell>
          </TableRow>
          <TableRow>
            <TableCell sx={{ fontWeight: 'bold', backgroundColor: '#f8fafc' }}>Request Department</TableCell>
            <TableCell>{project.department}</TableCell>
            <TableCell sx={{ fontWeight: 'bold', backgroundColor: '#f8fafc' }}>Requester</TableCell>
            <TableCell>{project.requester || project.owner}</TableCell>
          </TableRow>
          <TableRow>
            <TableCell sx={{ fontWeight: 'bold', backgroundColor: '#f8fafc' }}>Position</TableCell>
            <TableCell>{project.position || 'Engineer'}</TableCell>
            <TableCell sx={{ fontWeight: 'bold', backgroundColor: '#f8fafc' }}>Contact</TableCell>
            <TableCell>{project.contact || ''}</TableCell>
          </TableRow>
        </TableBody>
      </Table>

      {/* B. IMPROVEMENT INFORMATION */}
      <Typography variant="subtitle2" sx={{ fontWeight: 'bold', backgroundColor: '#e2e8f0', p: 0.5, mb: 1 }}>
        B. IMPROVEMENT INFORMATION (개선 정보)
      </Typography>
      <Table size="small" sx={{ mb: 2, '& td': { border: '1px solid #cbd5e1', p: 0.8, fontSize: '0.85rem' } }}>
        <TableBody>
          <TableRow>
            <TableCell sx={{ fontWeight: 'bold', width: '25%', backgroundColor: '#f8fafc' }}>Improvement Category</TableCell>
            <TableCell colSpan={3}>
              <Box sx={{ display: 'flex', gap: 2 }}>
                {['Productivity', 'Quality', 'Cost Saving', 'Equipment', 'Safety / Environment', 'Others'].map((cat) => (
                  <Box key={cat} sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
                    <input type="checkbox" checked={project.category === cat || (cat === 'Cost Saving' && project.category === 'Cost')} readOnly />
                    <Typography variant="caption" sx={{ fontWeight: project.category === cat ? 'bold' : 'normal' }}>{cat}</Typography>
                  </Box>
                ))}
              </Box>
            </TableCell>
          </TableRow>
          <TableRow>
            <TableCell sx={{ fontWeight: 'bold', backgroundColor: '#f8fafc' }}>Issue Description</TableCell>
            <TableCell colSpan={3}>{project.issue_description || 'N/A'}</TableCell>
          </TableRow>
          <TableRow>
            <TableCell sx={{ fontWeight: 'bold', backgroundColor: '#f8fafc' }}>Current Status</TableCell>
            <TableCell colSpan={3}>{project.current_status || `Before value: ${project.before_value ?? 'N/A'}`}</TableCell>
          </TableRow>
          <TableRow>
            <TableCell sx={{ fontWeight: 'bold', backgroundColor: '#f8fafc' }}>Target</TableCell>
            <TableCell colSpan={3}>{project.target_description || `Target value: ${project.target_value ?? 'N/A'}`}</TableCell>
          </TableRow>
          <TableRow>
            <TableCell sx={{ fontWeight: 'bold', backgroundColor: '#f8fafc' }}>Expected Benefit</TableCell>
            <TableCell colSpan={3}>{project.expected_benefit || `Expected Cost Saving: $${project.cost_saving ?? 0}`}</TableCell>
          </TableRow>
          <TableRow>
            <TableCell sx={{ fontWeight: 'bold', backgroundColor: '#f8fafc' }}>Related Process / Equipment</TableCell>
            <TableCell colSpan={3}>{project.related_process || project.process_area}</TableCell>
          </TableRow>
          <TableRow>
            <TableCell sx={{ fontWeight: 'bold', backgroundColor: '#f8fafc' }}>Requested Due Date</TableCell>
            <TableCell colSpan={3}>{project.due_date}</TableCell>
          </TableRow>
        </TableBody>
      </Table>

      {/* C. TPM REVIEW */}
      <Typography variant="subtitle2" sx={{ fontWeight: 'bold', backgroundColor: '#e2e8f0', p: 0.5, mb: 1 }}>
        C. TPM REVIEW
      </Typography>
      <Table size="small" sx={{ mb: 2, '& td': { border: '1px solid #cbd5e1', p: 0.8, fontSize: '0.85rem' } }}>
        <TableBody>
          <TableRow>
            <TableCell sx={{ fontWeight: 'bold', width: '20%', backgroundColor: '#f8fafc' }}>Reviewed By</TableCell>
            <TableCell sx={{ width: '30%' }}>{project.tpm_reviewed_by || ''}</TableCell>
            <TableCell sx={{ fontWeight: 'bold', width: '20%', backgroundColor: '#f8fafc' }}>Review Date</TableCell>
            <TableCell sx={{ width: '30%' }}>{project.tpm_review_date || ''}</TableCell>
          </TableRow>
          <TableRow>
            <TableCell sx={{ fontWeight: 'bold', backgroundColor: '#f8fafc' }}>Priority</TableCell>
            <TableCell colSpan={3}>
              <Box sx={{ display: 'flex', gap: 3 }}>
                <Typography variant="body2" sx={{ color: project.priority === 'High' ? 'red' : 'inherit', fontWeight: project.priority === 'High' ? 'bold' : 'normal' }}>
                  {project.priority === 'High' ? '■' : '□'} High
                </Typography>
                <Typography variant="body2" sx={{ color: project.priority === 'Medium' ? 'orange' : 'inherit', fontWeight: project.priority === 'Medium' ? 'bold' : 'normal' }}>
                  {project.priority === 'Medium' ? '■' : '□'} Medium
                </Typography>
                <Typography variant="body2" sx={{ color: project.priority === 'Low' ? 'green' : 'inherit', fontWeight: project.priority === 'Low' ? 'bold' : 'normal' }}>
                  {project.priority === 'Low' ? '■' : '□'} Low
                </Typography>
              </Box>
            </TableCell>
          </TableRow>
          <TableRow>
            <TableCell sx={{ fontWeight: 'bold', backgroundColor: '#f8fafc' }}>Review Comment</TableCell>
            <TableCell colSpan={3}>{project.tpm_review_comment || ''}</TableCell>
          </TableRow>
          <TableRow>
            <TableCell sx={{ fontWeight: 'bold', backgroundColor: '#f8fafc' }}>Decision</TableCell>
            <TableCell colSpan={3}>
              <Box sx={{ display: 'flex', gap: 4 }}>
                <Typography variant="body2" sx={{ color: 'blue', fontWeight: 'bold' }}>
                  {project.tpm_decision === 'Not Approved' ? '□' : '■'} Approved
                </Typography>
                <Typography variant="body2" sx={{ color: 'red', fontWeight: 'bold' }}>
                  {project.tpm_decision === 'Not Approved' ? '■' : '□'} Not Approved
                </Typography>
              </Box>
            </TableCell>
          </TableRow>
        </TableBody>
      </Table>
      <Typography variant="caption" sx={{ fontStyle: 'italic', color: '#64748b', display: 'block', textAlign: 'center' }}>
        * Approved 시 CI Project로 진행하며, 미승인 시 관련 부서에서 시정조치 절차에 따라 처리합니다.
      </Typography>
    </Box>
  );
}
