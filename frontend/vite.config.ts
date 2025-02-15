import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    host: true,
    proxy: {
      "/api": "http://127.0.0.1:5000",
      "/login/google": "http://127.0.0.1:5000",
      "/login/google/authorized": "http://127.0.0.1:5000",
    },
  },
});
