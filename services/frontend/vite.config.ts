import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

// Dev only: the browser calls relative /api/... and Vite forwards it to the API.
// In containers, nginx does this same job (phase 3b), so the app code never changes.
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': process.env.API_URL ?? 'http://localhost:8000',
    },
  },
})
