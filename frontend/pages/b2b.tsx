import Head from 'next/head'
import Navbar from '../components/Navbar'
import { Container, Typography, TextField, Button } from '@mui/material'
import FadeIn from '../components/FadeIn'

export default function B2B() {
  return (
    <>
      <Head><title>Для клиник</title></Head>
      <Navbar />
      <FadeIn>
      <Container sx={{py:5}}>
        <Typography variant="h4" gutterBottom>Интеграция для ветеринарных клиник</Typography>
        <Typography gutterBottom>Свяжитесь с нами для подключения Scanimal к вашей системе.</Typography>
        <TextField label="Название клиники" fullWidth sx={{my:1}} />
        <TextField label="Email" type="email" fullWidth sx={{my:1}} />
        <Button variant="contained" color="primary">Отправить</Button>
      </Container>
      </FadeIn>
    </>
  )
}
