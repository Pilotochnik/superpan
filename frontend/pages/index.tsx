import Head from 'next/head'
import { Container, Typography, Button, Box, List, ListItem, Alert } from '@mui/material'
import Navbar from '../components/Navbar'
import Link from 'next/link'

export default function Home() {
  return (
    <>
      <Head>
        <title>Scanimal</title>
      </Head>
      <Navbar />
      <Container sx={{py:5}}>
        <Typography variant="h3" gutterBottom>VetEra Scanimal</Typography>
        <Typography gutterBottom>
          AI-powered analysis of cat X-ray images. Upload a scan and get an instant assessment.
        </Typography>
        <Button variant="contained" color="primary" component={Link} href="/analyze">
          Upload X-ray
        </Button>
        <Box sx={{my:4}}>
          <Typography variant="h5">How it works</Typography>
          <List>
            <ListItem>1. Upload your cat's X-ray image</ListItem>
            <ListItem>2. Scanimal analyzes it with AI</ListItem>
            <ListItem>3. View the result and consult your vet</ListItem>
          </List>
        </Box>
        <Alert severity="warning">This is not a diagnosis. Always consult a veterinarian.</Alert>
      </Container>
    </>
  )
}
