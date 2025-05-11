// Vite proxy config for development
// Place this file in src/frontend/src/

export default {
  server: {
    proxy: {
      '/api': 'http://localhost:8000',
    },
  },
}; 