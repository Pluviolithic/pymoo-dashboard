// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2024-04-03',
  css: ['~/assets/css/main.css'],
  devtools: { enabled: true },
  runtimeConfig: {
	public: {
		WS_URL: 'localhost:5000',
	}
  },
  nitro: {
    routeRules: {
      '/listen': { proxy: 'http://localhost:5000/listen'}
    }
  }
})