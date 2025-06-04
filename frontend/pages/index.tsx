import Head from 'next/head'
import { Container, Typography, Button, Box, List, ListItem, Alert } from '@mui/material'
import Navbar from '../components/Navbar'
import Link from 'next/link'
import FadeIn from '../components/FadeIn'

export default function Home() {
  return (
    <>
      <Head>
        <title>Scanimal</title>
      </Head>
      <Navbar />
      <FadeIn>
        <Container sx={{py:5}}>
          <Typography variant="h3" gutterBottom>VetEra Scanimal</Typography>
          <Typography gutterBottom>
            ИИ-анализ рентгеновских снимков кошек. Загрузите изображение и получите быстрый результат.
          </Typography>
          <Button variant="contained" color="primary" component={Link} href="/analyze">
            Загрузить снимок
          </Button>
          <Box sx={{my:4}}>
            <Typography variant="h5">Как это работает</Typography>
            <List>
              <ListItem>1. Загрузите рентген</ListItem>
              <ListItem>2. Система анализирует снимок</ListItem>
              <ListItem>3. Получите результат и обратитесь к ветеринару</ListItem>
            </List>
          </Box>
          <Alert severity="warning">Это не диагноз. Обратитесь к специалисту.</Alert>
        </Container>
      </FadeIn>
    </>
  )
}
