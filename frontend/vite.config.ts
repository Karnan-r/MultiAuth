import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    host: true, // Ensures Vite runs on all network interfaces
  },
  build: {
    outDir: "dist", // Ensure Vercel picks the correct build directory
  },
  resolve: {
    alias: {
      '@': '/src', // Optional alias for cleaner imports
    },
  },
});







// import { defineConfig } from 'vite'
// import react from '@vitejs/plugin-react'

// export default defineConfig({
//   plugins: [react()],
//   server: {
//     port: 5173,
//     host: true,
//     proxy: {
//       "/api": "http://127.0.0.1:5000",
//       "/login/google": "http://127.0.0.1:5000",
//       "/login/google/authorized": "http://127.0.0.1:5000",
//     },
//   },
// });
