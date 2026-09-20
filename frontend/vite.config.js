import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  // The repo keeps a single .env at its root (see .env.example), not one per
  // package, so Vite is pointed up a level to find VITE_API_BASE_URL.
  envDir: '..',
  server: { port: 5173 },
});
