import Link from 'next/link'
import { AppBar, Toolbar, Typography, Box, Button } from '@mui/material'
import Image from 'next/image'

export default function Navbar() {
  return (
    <AppBar position="static" color="transparent" sx={{borderBottom: '1px solid #444'}}>
      <Toolbar>
        <Link href="/" passHref style={{display:'flex',alignItems:'center',textDecoration:'none'}}>
          <Image src="/logo.svg" alt="Scanimal" width={32} height={32} />
          <Typography variant="h6" sx={{ml:1,color:'#0ff'}}>Scanimal</Typography>
        </Link>
        <Box sx={{flexGrow:1}} />
        <Button color="inherit" component={Link} href="/analyze">Analyze</Button>
        <Button color="inherit" component={Link} href="/dashboard">Dashboard</Button>
        <Button color="inherit" component={Link} href="/b2b">For Clinics</Button>
      </Toolbar>
    </AppBar>
  )
}
