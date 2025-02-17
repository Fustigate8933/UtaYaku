// https://nuxt.com/docs/api/configuration/nuxt-config
import fs from 'node:fs'
import path from 'node:path'

export default defineNuxtConfig({
	devServer: {
		port: 80,
		host: "0.0.0.0"
	},

	runtimeConfig: {
		private: {
			CLIENT_ID: process.env.CLIENT_ID,
			DB_URL: process.env.DB_URL,
			SUPABASE_URL: process.env.SUPABASE_URL,
			SUPABASE_KEY: process.env.SUPABASE_KEY,
			SUPABASE_SERVICE_KEY: process.env.SUPABASE_SERVICE_KEY,
		}
	},

	supabase: {
		redirect: false
	},

	compatibilityDate: '2024-04-03',
	devtools: { enabled: true },

	future: {
		compatibilityVersion: 4
	},

	modules: [
		"@nuxtjs/tailwindcss",
		"@nuxt/fonts",
		"@nuxt/icon",
		"@nuxt/image",
		"@nuxtjs/supabase"
	],

	css: ["./assets/css/tailwind.css"],

	fonts: {
		families: [
			{name: "Roboto Mono", provider: "fontsource"}
		]
	},

	hooks: {
    'build:done'() {
      const sourceDir = path.resolve(__dirname, 'node_modules/kuromoji/dict');
      const destinationDir = path.resolve(__dirname, '.output/server/node_modules/kuromoji/dict');

			console.log('Source Directory:', sourceDir);
			console.log('Destination Directory:', destinationDir);

			if (!fs.existsSync(sourceDir)) {
				console.error('Source directory does not exist:', sourceDir);
				return;
			}

			if (!fs.existsSync(destinationDir)) {
				console.log('Creating destination directory:', destinationDir);
				fs.mkdirSync(destinationDir, { recursive: true });
			}

			fs.cpSync(sourceDir, destinationDir, { recursive: true });
      console.log('Kuromoji dictionary files copied successfully.');
    },
  }
})
