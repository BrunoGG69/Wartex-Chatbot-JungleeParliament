import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      // Proxy to your local backend during development
      '/api': 'http://localhost:5000'
    }
  }
})
