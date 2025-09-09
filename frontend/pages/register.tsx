import Head from 'next/head'
import Navbar from '../components/Navbar'
import { Container, Typography, TextField, Button } from '@mui/material'
import { useState } from 'react'
import { useRouter } from 'next/router'
import FadeIn from '../components/FadeIn'

export default function Register() {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const router = useRouter()

  const submit = async () => {
    const res = await fetch('http://localhost:8000/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password }),
    })
    if (res.ok) {
      router.push('/login')
    }
  }

  return (
    <>
      <Head><title>Регистрация</title></Head>
      <Navbar />
      <FadeIn>
        <Container sx={{py:5}}>
          <Typography variant="h4" gutterBottom>Регистрация</Typography>
          <TextField label="Имя пользователя" fullWidth sx={{my:1}} value={username} onChange={e=>setUsername(e.target.value)} />
          <TextField label="Пароль" type="password" fullWidth sx={{my:1}} value={password} onChange={e=>setPassword(e.target.value)} />
          <Button variant="contained" onClick={submit}>Создать аккаунт</Button>
        </Container>
      </FadeIn>
    </>
  )
}
