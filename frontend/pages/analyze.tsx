import { useState } from 'react'
import Head from 'next/head'
import Navbar from '../components/Navbar'
import { Container, Typography, Box, Button, LinearProgress } from '@mui/material'

export default function Analyze() {
  const [file, setFile] = useState<File | null>(null)
  const [result, setResult] = useState<any>(null)
  const [loading, setLoading] = useState(false)

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0])
    }
  }

  const submit = async () => {
    if (!file) return
    const formData = new FormData()
    formData.append('file', file)
    setLoading(true)
    const res = await fetch('http://localhost:8000/analyze', {
      method: 'POST',
      body: formData,
    })
    const data = await res.json()
    setResult(data)
    setLoading(false)
  }

  return (
    <>
      <Head><title>Analyze</title></Head>
      <Navbar />
      <Container sx={{py:5}}>
        <Typography variant="h4" gutterBottom>Analyze X-ray</Typography>
        <input type="file" accept="image/*" onChange={handleFileChange} />
        <Button variant="contained" sx={{ml:2}} onClick={submit}>Send</Button>
        {loading && <LinearProgress sx={{my:2}}/>}
        {result && (
          <Box sx={{mt:2}}>
            <Typography variant="h6">Result: {result.top_class}</Typography>
            <Typography>{result.description}</Typography>
            <ul>
              {result.predictions.map((p:any) => (
                <li key={p.label}>{p.label}: {(p.probability*100).toFixed(1)}%</li>
              ))}
            </ul>
          </Box>
        )}
      </Container>
    </>
  )
}
