import { createTheme } from '@mui/material/styles';

export const getAppTheme = (mode = 'light') =>
  createTheme({
    palette: {
      mode,
      primary: {
        main: '#1565C0', // SAP Fiori / Power BI Blue
        light: '#42a5f5',
        dark: '#0d47a1',
        contrastText: '#ffffff',
      },
      secondary: {
        main: '#0288D1',
        light: '#03a9f4',
        dark: '#01579b',
      },
      background: {
        default: mode === 'light' ? '#f4f6f9' : '#0f172a',
        paper: mode === 'light' ? '#ffffff' : '#1e293b',
      },
      success: {
        main: '#2E7D32',
        light: '#4caf50',
      },
      warning: {
        main: '#ED6C02',
        light: '#ff9800',
      },
      error: {
        main: '#D32F2F',
        light: '#ef5350',
      },
      info: {
        main: '#0288D1',
      },
    },
    typography: {
      fontFamily: ['Inter', 'Roboto', 'sans-serif'].join(','),
      h5: {
        fontWeight: 700,
      },
      h6: {
        fontWeight: 600,
      },
      subtitle1: {
        fontWeight: 600,
      },
    },
    components: {
      MuiCard: {
        styleOverrides: {
          root: {
            borderRadius: 8,
            boxShadow: mode === 'light'
              ? '0px 2px 4px rgba(0, 0, 0, 0.05), 0px 1px 2px rgba(0, 0, 0, 0.1)'
              : '0px 2px 4px rgba(0, 0, 0, 0.3)',
          },
        },
      },
      MuiButton: {
        styleOverrides: {
          root: {
            textTransform: 'none',
            fontWeight: 600,
            borderRadius: 6,
          },
        },
      },
      MuiTableCell: {
        styleOverrides: {
          head: {
            fontWeight: 700,
            backgroundColor: mode === 'light' ? '#f1f5f9' : '#334155',
          },
        },
      },
    },
  });
