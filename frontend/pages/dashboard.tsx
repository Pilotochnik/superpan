import Head from 'next/head'
import Navbar from '../components/Navbar'
import { Container, Typography } from '@mui/material'

export default function Dashboard() {
  return (
    <>
      <Head><title>Dashboard</title></Head>
      <Navbar />
      <Container sx={{py:5}}>
        <Typography variant="h4">Dashboard</Typography>
        <Typography>History coming soon.</Typography>
      </Container>
    </>
  )
}
