import { createTheme } from '@mui/material/styles'

const theme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#00bcd4', // emerald
    },
    secondary: {
      main: '#ffeb3b', // yellow accent
    },
    background: {
      default: '#001e3c',
      paper: '#0a1929',
    },
  },
})

export default theme
