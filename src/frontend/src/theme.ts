import { createTheme } from '@mui/material/styles';
import { PaletteMode } from '@mui/material';
import React from 'react';

export const ColorModeContext = React.createContext({ toggleColorMode: () => {} });

export const getTheme = (mode: PaletteMode) =>
  createTheme({
    palette: {
      mode,
      primary: {
        main: '#8e24aa', // purple
      },
      secondary: {
        main: '#ff9800', // orange
      },
    },
    shape: {
      borderRadius: 8,
    },
    typography: {
      fontFamily: 'Roboto, Arial, sans-serif',
    },
  }); 