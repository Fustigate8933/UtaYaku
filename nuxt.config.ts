// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
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
	}
})
