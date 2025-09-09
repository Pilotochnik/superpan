import Link from 'next/link'
import { AppBar, Toolbar, Typography, Box, Button } from '@mui/material'
import Image from 'next/image'
import { useContext } from 'react'
import { AuthContext } from './AuthProvider'

export default function Navbar() {
  const { user, logout } = useContext(AuthContext)
  return (
    <AppBar position="static" color="transparent" sx={{borderBottom: '1px solid #444'}}>
      <Toolbar>
        <Link href="/" passHref style={{display:'flex',alignItems:'center',textDecoration:'none'}}>
          <Image src="/logo.svg" alt="Scanimal" width={32} height={32} />
          <Typography variant="h6" sx={{ml:1,color:'#0ff'}}>Scanimal</Typography>
        </Link>
        <Box sx={{flexGrow:1}} />
        <Button color="inherit" component={Link} href="/analyze">Анализ</Button>
        <Button color="inherit" component={Link} href="/dashboard">Личный кабинет</Button>
        <Button color="inherit" component={Link} href="/b2b">Для клиник</Button>
        {user ? (
          <>
            <Typography sx={{mx:1}}>{user}</Typography>
            <Button color="inherit" onClick={logout}>Выход</Button>
          </>
        ) : (
          <>
            <Button color="inherit" component={Link} href="/login">Вход</Button>
            <Button color="inherit" component={Link} href="/register">Регистрация</Button>
          </>
        )}
      </Toolbar>
    </AppBar>
  )
}
