// filepath: d:\CTAE New\CTAE\CLTAE Nots\CTAE sem-8\Research Asssistant\GitHub\lexify_research_assistant_backend\frontend\vite.config.ts
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { fileURLToPath, URL } from 'node:url' // Import URL and fileURLToPath

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: { 
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  optimizeDeps: { 
    include: ['vue-router'],
    force: true // Add this line to force re-bundling
  }
})