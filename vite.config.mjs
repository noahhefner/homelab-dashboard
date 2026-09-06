import { defineConfig } from 'vite';
import { resolve } from 'node:path';

export default defineConfig({
  // URLs generated inside CSS/JS assets will be rooted at /static/.
  base: '/static/',

  build: {
    outDir: resolve(import.meta.dirname, 'app/static'),
    emptyOutDir: true,
    manifest: false,

    rollupOptions: {
      input: resolve(import.meta.dirname, 'assets/app.js'),

      output: {
        entryFileNames: 'js/app-[hash].js',
        chunkFileNames: 'js/[name]-[hash].js',

        assetFileNames: (assetInfo) => {
          const name = assetInfo.name ?? '';

          if (name.endsWith('.css')) {
            return 'css/[name]-[hash][extname]';
          }

          if (/\.(woff2?|ttf|otf|eot)$/.test(name)) {
            return 'fonts/[name]-[hash][extname]';
          }

          return 'assets/[name]-[hash][extname]';
        },
      },
    },


  },

  plugins: [
    {
      name: 'generate-asset-manifest',

      generateBundle(_options, bundle) {
        const manifest = {
          js: [],
          css: [],
        };

        for (const [filename, output] of Object.entries(bundle)) {
          if (output.type === 'chunk' && filename.endsWith('.js')) {
            manifest.js.push(filename);
          }

          if (output.type === 'asset' && filename.endsWith('.css')) {
            manifest.css.push(filename);
          }
        }

        this.emitFile({
          type: 'asset',
          fileName: 'manifest.json',
          source: JSON.stringify(manifest, null, 2) + '\n',
        });
      },
    },


  ],
});