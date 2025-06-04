import Head from 'next/head'
import Navbar from '../components/Navbar'
import { Container, Typography, TextField, Button } from '@mui/material'

export default function B2B() {
  return (
    <>
      <Head><title>For Clinics</title></Head>
      <Navbar />
      <Container sx={{py:5}}>
        <Typography variant="h4" gutterBottom>Integration for Clinics</Typography>
        <Typography gutterBottom>Contact us to integrate Scanimal into your system.</Typography>
        <TextField label="Clinic Name" fullWidth sx={{my:1}} />
        <TextField label="Email" type="email" fullWidth sx={{my:1}} />
        <Button variant="contained" color="primary">Send Request</Button>
      </Container>
    </>
  )
}
