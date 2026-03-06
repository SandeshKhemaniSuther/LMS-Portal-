import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import { resolve } from 'path';

export default defineConfig({
    plugins: [vue()],
    build: {
        outDir: 'public',
        emptyOutDir: true,
        rollupOptions: {
            input: {
                main: resolve(__dirname, 'resources/js/app.js')
            },
            output: {
                manualChunks: {
                    vendor: ['vue', 'vue-router', 'axios'],
                }
            }
        }
    },
    server: {
        host: '0.0.0.0',
        port: 3000,
        proxy: {
            '/api': {
                target: 'http://localhost:8000',
                changeOrigin: true,
                secure: false
            }
        }
    },
    publicDir: 'public'
});
