import Head from 'next/head'
import Navbar from '../components/Navbar'
import { Container, Typography } from '@mui/material'

export default function Policy() {
  return (
    <>
      <Head><title>Data Policy</title></Head>
      <Navbar />
      <Container sx={{py:5}}>
        <Typography variant="h4">Data Policy</Typography>
        <Typography>We respect your privacy. Uploaded images are stored securely and used only for analysis.</Typography>
      </Container>
    </>
  )
}
