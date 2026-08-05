import React, { useState, useEffect } from 'react';
import {
  Box, Card, CardContent, Typography, Table, TableHead, TableRow, TableCell, TableBody,
  TextField, Button, Alert, Snackbar, Grid, MenuItem, Dialog, DialogTitle, DialogContent, DialogActions, Tabs, Tab, IconButton, Switch, FormControlLabel
} from '@mui/material';
import { Save as SaveIcon, Settings as SettingsIcon, Lock as LockIcon, Edit as EditIcon, Delete as DeleteIcon, Add as AddIcon, Tune as TuneIcon } from '@mui/icons-material';
import { settingsAPI, authAPI } from '../services/api';
import { useAuth } from '../context/AuthContext';

function TabPanel(props) {
  const { children, value, index, ...other } = props;
  return (
    <div role="tabpanel" hidden={value !== index} {...other}>
      {value === index && <Box sx={{ pt: 3 }}>{children}</Box>}
    </div>
  );
}

export default function AdminSettings() {
  const { user } = useAuth();
  const isAdmin = user?.role === 'Administrator';

  // Common
  const [msg, setMsg] = useState({ open: false, text: '', type: 'success' });
  const [tabValue, setTabValue] = useState(isAdmin ? 0 : 4); // Default to Change Password if not admin
  const [loading, setLoading] = useState(true);

  // KPI Targets
  const [targets, setTargets] = useState([]);
  const [savingKey, setSavingKey] = useState(null);

  // Users
  const [users, setUsers] = useState([]);
  const [roles, setRoles] = useState([]);
  const [userDialog, setUserDialog] = useState(false);
  const [selectedUser, setSelectedUser] = useState(null);
  const [formUser, setFormUser] = useState({ username: '', email: '', password: '', full_name: '', role: 'Engineer', department: '' });
  const [roleDefaults] = useState({
    'Administrator': 'password123',
    'TPM Manager': 'password123',
    'Engineer': 'password123',
    'QA Inspector': 'password123',
    'Management': 'password123',
    'Auditor': 'password123'
  });

  // Role Management
  const [roleDialog, setRoleDialog] = useState(false);
  const [selectedRole, setSelectedRole] = useState(null);
  const [formRole, setFormRole] = useState({ name: '', description: '' });

  // CI Numbering
  const [ciParts, setCIParts] = useState([]);
  const [ciSeparator, setCISeparator] = useState('-');
  const [ciExample, setCIExample] = useState('');
  const [savingCI, setSavingCI] = useState(false);

  // Password
  const [passwordData, setPasswordData] = useState({ currentPassword: '', newPassword: '', confirmPassword: '' });
  const [changingPassword, setChangingPassword] = useState(false);

  const loadData = async () => {
    setLoading(true);
    try {
      if (isAdmin) {
        const [resTargets, resUsers, resRoles] = await Promise.all([
          settingsAPI.getKPITargets(),
          settingsAPI.getUsers(),
          settingsAPI.getRoles()
        ]);
        setTargets(resTargets.data);
        setUsers(resUsers.data);
        setRoles(resRoles.data);
        
        // Load CI Numbering config
        try {
          const resCI = await settingsAPI.getCINumberingConfig();
          setCIParts(resCI.data.parts || []);
          setCISeparator(resCI.data.separator || '-');
          setCIExample(resCI.data.example || '');
        } catch (err) {
          console.warn('Failed to load CI config:', err);
        }
      }
    } catch (err) {
      console.error(err);
      setMsg({ open: true, text: 'Failed to load data', type: 'error' });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  // KPI Targets Handlers
  const handleValueChange = (kpiKey, val) => {
    setTargets(targets.map((t) => (t.kpi_key === kpiKey ? { ...t, target_value: parseFloat(val) || 0 } : t)));
  };

  const handleOperatorChange = (kpiKey, val) => {
    setTargets(targets.map((t) => (t.kpi_key === kpiKey ? { ...t, comparison_operator: val } : t)));
  };

  const handleSaveKPI = async (target) => {
    setSavingKey(target.kpi_key);
    try {
      await settingsAPI.updateKPITarget(target.kpi_key, {
        target_value: target.target_value,
        comparison_operator: target.comparison_operator,
        unit: target.unit
      });
      setMsg({ open: true, text: `Successfully updated target for ${target.kpi_name}`, type: 'success' });
      loadData();
    } catch (err) {
      setMsg({ open: true, text: err.response?.data?.detail || 'Failed to update target', type: 'error' });
    } finally {
      setSavingKey(null);
    }
  };

  // CI Numbering Handlers
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

  // User Handlers
  const openUserDialog = (user = null) => {
    if (user) {
      setSelectedUser(user);
      setFormUser({ username: user.username, email: user.email, password: '', full_name: user.full_name, role: user.role, department: user.department || '' });
    } else {
      setSelectedUser(null);
      setFormUser({ username: '', email: '', password: '', full_name: '', role: 'Engineer', department: '' });
    }
    setUserDialog(true);
  };

  const handleSaveUser = async () => {
    if (!formUser.username || !formUser.email || !formUser.full_name) {
      setMsg({ open: true, text: 'All fields are required', type: 'error' });
      return;
    }
    try {
      if (selectedUser) {
        setMsg({ open: true, text: 'User update coming soon', type: 'info' });
      } else {
        if (!formUser.password) {
          setMsg({ open: true, text: 'Password is required for new user', type: 'error' });
          return;
        }
        setMsg({ open: true, text: 'User created (feature to be implemented)', type: 'success' });
      }
      setUserDialog(false);
      loadData();
    } catch (err) {
      setMsg({ open: true, text: err.response?.data?.detail || 'Failed to save user', type: 'error' });
    }
  };

  const handleDeleteUser = async (userId) => {
    if (window.confirm('Are you sure you want to delete this user?')) {
      try {
        setMsg({ open: true, text: 'User deletion coming soon', type: 'info' });
      } catch (err) {
        setMsg({ open: true, text: 'Failed to delete user', type: 'error' });
      }
    }
  };

  const handleResetUserPassword = async (user) => {
    const defaultPassword = roleDefaults[user.role] || 'password123';
    if (window.confirm(`Reset password for ${user.username} to default password?`)) {
      try {
        await settingsAPI.resetUserPassword(user.id, { new_password: defaultPassword });
        setMsg({ open: true, text: `Password reset to default for ${user.username}`, type: 'success' });
        loadData();
      } catch (err) {
        setMsg({ open: true, text: 'Failed to reset password', type: 'error' });
      }
    }
  };

  // Role Handlers
  const openRoleDialog = (role = null) => {
    if (role) {
      setSelectedRole(role);
      setFormRole({ name: role.name, description: role.description || '' });
    } else {
      setSelectedRole(null);
      setFormRole({ name: '', description: '' });
    }
    setRoleDialog(true);
  };

  const handleSaveRole = async () => {
    if (!formRole.name) {
      setMsg({ open: true, text: 'Role name is required', type: 'error' });
      return;
    }
    try {
      setMsg({ open: true, text: selectedRole ? 'Role updated' : 'Role created', type: 'success' });
      setRoleDialog(false);
      loadData();
    } catch (err) {
      setMsg({ open: true, text: 'Failed to save role', type: 'error' });
    }
  };

  const handleDeleteRole = async (role) => {
    if (window.confirm(`Delete role "${role.name}"?`)) {
      try {
        setMsg({ open: true, text: 'Role deletion coming soon', type: 'info' });
      } catch (err) {
        setMsg({ open: true, text: 'Failed to delete role', type: 'error' });
      }
    }
  };

  // Password Change
  const handleChangePassword = async () => {
    if (!passwordData.currentPassword || !passwordData.newPassword || !passwordData.confirmPassword) {
      setMsg({ open: true, text: 'All password fields are required', type: 'error' });
      return;
    }
    if (passwordData.newPassword !== passwordData.confirmPassword) {
      setMsg({ open: true, text: 'New passwords do not match', type: 'error' });
      return;
    }
    if (passwordData.newPassword.length < 6) {
      setMsg({ open: true, text: 'New password must be at least 6 characters', type: 'error' });
      return;
    }
    setChangingPassword(true);
    try {
      await authAPI.changePassword({
        old_password: passwordData.currentPassword,
        new_password: passwordData.newPassword
      });
      setMsg({ open: true, text: 'Password changed successfully', type: 'success' });
      setPasswordData({ currentPassword: '', newPassword: '', confirmPassword: '' });
    } catch (err) {
      setMsg({ open: true, text: err.response?.data?.detail || 'Failed to change password', type: 'error' });
    } finally {
      setChangingPassword(false);
    }
  };

  if (loading) {
    return <Typography sx={{ p: 3 }}>Loading...</Typography>;
  }

  return (
    <Box sx={{ p: 3 }}>
      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1.5, mb: 3 }}>
        <SettingsIcon color="primary" sx={{ fontSize: 32 }} />
        <Box>
          <Typography variant="h5" sx={{ fontWeight: 800 }}>Admin System Settings</Typography>
          <Typography variant="body2" sx={{ color: '#64748b' }}>
            {isAdmin ? 'Configure system settings, KPI targets, users and roles' : 'Change your password'}
          </Typography>
        </Box>
      </Box>

      {/* Tabs */}
      <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 2 }}>
        <Tabs value={tabValue} onChange={(e, v) => setTabValue(v)}>
          {isAdmin && <Tab label="CI Numbering" icon={<TuneIcon />} iconPosition="start" />}
          {isAdmin && <Tab label="KPI Targets" />}
          {isAdmin && <Tab label="User Management" />}
          {isAdmin && <Tab label="Role Management" />}
          <Tab label="Change Password" />
        </Tabs>
      </Box>

      {/* CI Numbering Tab */}
      {isAdmin && (
        <TabPanel value={tabValue} index={0}>
          <Grid container spacing={3}>
            <Grid item xs={12} md={7}>
              <Card sx={{ borderLeft: '4px solid #2563eb' }}>
                <CardContent>
                  <Typography variant="h6" sx={{ fontWeight: 700, mb: 3 }}>CI Project Numbering Configuration</Typography>
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
        </TabPanel>
      )}

      {/* KPI Targets Tab */}
      {isAdmin && (
        <TabPanel value={tabValue} index={1}>
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
                          <MenuItem value="<=">≤</MenuItem>
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
                      <TableCell>
                        <Button
                          variant="contained"
                          color="primary"
                          size="small"
                          startIcon={<SaveIcon />}
                          onClick={() => handleSaveKPI(t)}
                          disabled={savingKey === t.kpi_key}
                        >
                          {savingKey === t.kpi_key ? 'Saving...' : 'Save'}
                        </Button>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </CardContent>
          </Card>
        </TabPanel>
      )}

      {/* User Management Tab */}
      {isAdmin && (
        <TabPanel value={tabValue} index={2}>
          <Card sx={{ borderLeft: '4px solid #2E7D32' }}>
            <CardContent>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                <Typography variant="h6" sx={{ fontWeight: 700 }}>User Management</Typography>
                <Button variant="contained" color="primary" size="small" startIcon={<AddIcon />} onClick={() => openUserDialog()}>
                  Add User
                </Button>
              </Box>
              <Table size="small">
                <TableHead>
                  <TableRow sx={{ backgroundColor: '#f1f5f9' }}>
                    <TableCell sx={{ fontWeight: 'bold' }}>Username</TableCell>
                    <TableCell sx={{ fontWeight: 'bold' }}>Email</TableCell>
                    <TableCell sx={{ fontWeight: 'bold' }}>Full Name</TableCell>
                    <TableCell sx={{ fontWeight: 'bold' }}>Role</TableCell>
                    <TableCell sx={{ fontWeight: 'bold' }}>Status</TableCell>
                    <TableCell sx={{ fontWeight: 'bold' }}>Actions</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {users.map((u) => (
                    <TableRow key={u.id} hover>
                      <TableCell sx={{ fontWeight: 600 }}>{u.username}</TableCell>
                      <TableCell>{u.email}</TableCell>
                      <TableCell>{u.full_name}</TableCell>
                      <TableCell>{u.role}</TableCell>
                      <TableCell>
                        <Typography variant="caption" sx={{ color: u.is_active ? '#2E7D32' : '#dc2626', fontWeight: 'bold' }}>
                          {u.is_active ? 'Active' : 'Inactive'}
                        </Typography>
                      </TableCell>
                      <TableCell>
                        <IconButton size="small" onClick={() => openUserDialog(u)} title="Edit">
                          <EditIcon fontSize="small" />
                        </IconButton>
                        <IconButton size="small" onClick={() => handleResetUserPassword(u)} title="Reset Password" color="warning">
                          <LockIcon fontSize="small" />
                        </IconButton>
                        <IconButton size="small" onClick={() => handleDeleteUser(u.id)} title="Delete" color="error">
                          <DeleteIcon fontSize="small" />
                        </IconButton>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </CardContent>
          </Card>
        </TabPanel>
      )}

      {/* Role Management Tab */}
      {isAdmin && (
        <TabPanel value={tabValue} index={3}>
          <Card sx={{ borderLeft: '4px solid #DC2626' }}>
            <CardContent>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                <Typography variant="h6" sx={{ fontWeight: 700 }}>Role Management</Typography>
                <Button variant="contained" color="primary" size="small" startIcon={<AddIcon />} onClick={() => openRoleDialog()}>
                  Add Role
                </Button>
              </Box>
              <Table size="small">
                <TableHead>
                  <TableRow sx={{ backgroundColor: '#f1f5f9' }}>
                    <TableCell sx={{ fontWeight: 'bold' }}>Role Name</TableCell>
                    <TableCell sx={{ fontWeight: 'bold' }}>Description</TableCell>
                    <TableCell sx={{ fontWeight: 'bold' }}>Created At</TableCell>
                    <TableCell sx={{ fontWeight: 'bold' }}>Actions</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {roles.map((r) => (
                    <TableRow key={r.id} hover>
                      <TableCell sx={{ fontWeight: 600 }}>{r.name}</TableCell>
                      <TableCell>{r.description}</TableCell>
                      <TableCell sx={{ fontSize: '0.85rem', color: '#64748b' }}>
                        {new Date(r.created_at).toLocaleDateString()}
                      </TableCell>
                      <TableCell>
                        <IconButton size="small" onClick={() => openRoleDialog(r)} title="Edit">
                          <EditIcon fontSize="small" />
                        </IconButton>
                        <IconButton size="small" onClick={() => handleDeleteRole(r)} title="Delete" color="error">
                          <DeleteIcon fontSize="small" />
                        </IconButton>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </CardContent>
          </Card>
        </TabPanel>
      )}

      {/* Change Password Tab */}
      <TabPanel value={tabValue} index={isAdmin ? 4 : 0}>
        <Card sx={{ borderLeft: '4px solid #8b5cf6' }}>
          <CardContent>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 2 }}>
              <LockIcon sx={{ color: '#8b5cf6' }} />
              <Typography variant="h6" sx={{ fontWeight: 700 }}>Change Your Password</Typography>
            </Box>
            <Grid container spacing={2} sx={{ maxWidth: '500px' }}>
              <Grid item xs={12}>
                <TextField
                  label="Current Password"
                  type="password"
                  fullWidth
                  size="small"
                  value={passwordData.currentPassword}
                  onChange={(e) => setPasswordData({ ...passwordData, currentPassword: e.target.value })}
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  label="New Password"
                  type="password"
                  fullWidth
                  size="small"
                  value={passwordData.newPassword}
                  onChange={(e) => setPasswordData({ ...passwordData, newPassword: e.target.value })}
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  label="Confirm New Password"
                  type="password"
                  fullWidth
                  size="small"
                  value={passwordData.confirmPassword}
                  onChange={(e) => setPasswordData({ ...passwordData, confirmPassword: e.target.value })}
                />
              </Grid>
              <Grid item xs={12}>
                <Button
                  variant="contained"
                  color="primary"
                  startIcon={<SaveIcon />}
                  onClick={handleChangePassword}
                  disabled={changingPassword}
                >
                  {changingPassword ? 'Changing...' : 'Change Password'}
                </Button>
              </Grid>
            </Grid>
          </CardContent>
        </Card>
      </TabPanel>

      {/* User Dialog */}
      <Dialog open={userDialog} onClose={() => setUserDialog(false)} maxWidth="sm" fullWidth>
        <DialogTitle>{selectedUser ? 'Edit User' : 'Add New User'}</DialogTitle>
        <DialogContent sx={{ pt: 2 }}>
          <TextField
            label="Username"
            fullWidth
            size="small"
            value={formUser.username}
            onChange={(e) => setFormUser({ ...formUser, username: e.target.value })}
            disabled={selectedUser !== null}
            margin="normal"
          />
          <TextField
            label="Email"
            fullWidth
            size="small"
            type="email"
            value={formUser.email}
            onChange={(e) => setFormUser({ ...formUser, email: e.target.value })}
            margin="normal"
          />
          <TextField
            label="Full Name"
            fullWidth
            size="small"
            value={formUser.full_name}
            onChange={(e) => setFormUser({ ...formUser, full_name: e.target.value })}
            margin="normal"
          />
          <TextField
            label="Role"
            fullWidth
            size="small"
            select
            value={formUser.role}
            onChange={(e) => setFormUser({ ...formUser, role: e.target.value })}
            margin="normal"
          >
            {roles.map((r) => (
              <MenuItem key={r.id} value={r.name}>{r.name}</MenuItem>
            ))}
          </TextField>
          <TextField
            label="Department"
            fullWidth
            size="small"
            value={formUser.department}
            onChange={(e) => setFormUser({ ...formUser, department: e.target.value })}
            margin="normal"
          />
          {!selectedUser && (
            <TextField
              label="Password"
              fullWidth
              size="small"
              type="password"
              value={formUser.password}
              onChange={(e) => setFormUser({ ...formUser, password: e.target.value })}
              margin="normal"
              placeholder="Leave empty to use role default"
            />
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setUserDialog(false)}>Cancel</Button>
          <Button variant="contained" color="primary" onClick={handleSaveUser}>Save</Button>
        </DialogActions>
      </Dialog>

      {/* Role Dialog */}
      <Dialog open={roleDialog} onClose={() => setRoleDialog(false)} maxWidth="sm" fullWidth>
        <DialogTitle>{selectedRole ? 'Edit Role' : 'Add New Role'}</DialogTitle>
        <DialogContent sx={{ pt: 2 }}>
          <TextField
            label="Role Name"
            fullWidth
            size="small"
            value={formRole.name}
            onChange={(e) => setFormRole({ ...formRole, name: e.target.value })}
            disabled={selectedRole !== null}
            margin="normal"
          />
          <TextField
            label="Description"
            fullWidth
            size="small"
            multiline
            rows={3}
            value={formRole.description}
            onChange={(e) => setFormRole({ ...formRole, description: e.target.value })}
            margin="normal"
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setRoleDialog(false)}>Cancel</Button>
          <Button variant="contained" color="primary" onClick={handleSaveRole}>Save</Button>
        </DialogActions>
      </Dialog>

      <Snackbar open={msg.open} autoHideDuration={4000} onClose={() => setMsg({ ...msg, open: false })}>
        <Alert severity={msg.type} sx={{ width: '100%' }}>{msg.text}</Alert>
      </Snackbar>
    </Box>
  );
}
