import Head from 'next/head'
import Navbar from '../components/Navbar'
import { Container, Typography, TextField, Button } from '@mui/material'
import { useState, useContext } from 'react'
import { AuthContext } from '../components/AuthProvider'
import { useRouter } from 'next/router'
import FadeIn from '../components/FadeIn'

export default function Login() {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const { login } = useContext(AuthContext)
  const router = useRouter()

  const submit = async () => {
    const body = new URLSearchParams()
    body.append('username', username)
    body.append('password', password)
    const res = await fetch('http://localhost:8000/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: body.toString(),
    })
    if (res.ok) {
      const data = await res.json()
      login(data.access_token, username)
      router.push('/dashboard')
    }
  }

  return (
    <>
      <Head><title>Вход</title></Head>
      <Navbar />
      <FadeIn>
        <Container sx={{py:5}}>
          <Typography variant="h4" gutterBottom>Вход</Typography>
          <TextField label="Имя пользователя" fullWidth sx={{my:1}} value={username} onChange={e=>setUsername(e.target.value)} />
          <TextField label="Пароль" type="password" fullWidth sx={{my:1}} value={password} onChange={e=>setPassword(e.target.value)} />
          <Button variant="contained" onClick={submit}>Войти</Button>
        </Container>
      </FadeIn>
    </>
  )
}
