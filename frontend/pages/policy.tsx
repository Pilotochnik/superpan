import Head from 'next/head'
import Navbar from '../components/Navbar'
import { Container, Typography } from '@mui/material'
import FadeIn from '../components/FadeIn'

export default function Policy() {
  return (
    <>
      <Head><title>Политика данных</title></Head>
      <Navbar />
      <FadeIn>
        <Container sx={{py:5}}>
          <Typography variant="h4">Политика обработки данных</Typography>
          <Typography>Мы ценим вашу конфиденциальность. Загруженные изображения хранятся безопасно и используются только для анализа.</Typography>
        </Container>
      </FadeIn>
    </>
  )
}
