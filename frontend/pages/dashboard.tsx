import Head from 'next/head'
import Navbar from '../components/Navbar'
import { Container, Typography } from '@mui/material'
import { useContext, useEffect, useState } from 'react'
import { AuthContext } from '../components/AuthProvider'
import FadeIn from '../components/FadeIn'

export default function Dashboard() {
  const { token, user } = useContext(AuthContext)
  const [info, setInfo] = useState<any>(null)

  useEffect(() => {
    if (token) {
      fetch('http://localhost:8000/me', {
        headers: { Authorization: `Bearer ${token}` },
      })
        .then(res => res.json())
        .then(setInfo)
    }
  }, [token])

  return (
    <>
      <Head><title>Личный кабинет</title></Head>
      <Navbar />
      <FadeIn>
      <Container sx={{py:5}}>
        {token && info ? (
          <>
            <Typography variant="h4" gutterBottom>Привет, {info.username}!</Typography>
            <Typography>Здесь будет история анализов.</Typography>
          </>
        ) : (
          <Typography>Необходимо войти в систему.</Typography>
        )}
      </Container>
      </FadeIn>
    </>
  )
}
