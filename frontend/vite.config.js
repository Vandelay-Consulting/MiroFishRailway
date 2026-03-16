import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    port: 3000,
    open: true,
    allowedHosts: [
      'localhost',
      '127.0.0.1',
      '.railway.app',
      '.railway.internal'
    ],
    proxy: {
      '/api': {
        target: process.env.BACKEND_URL || 'http://localhost:5001',
        changeOrigin: true,
        secure: false,
        ws: true
      }
    },
    middlewareMode: false,
    hmr: {
      protocol: 'wss',
      host: process.env.RAILWAY_PUBLIC_DOMAIN || 'localhost',
      port: 443
    }
  }
})
