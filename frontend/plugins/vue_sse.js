// plugins/example-plugin.js
import VueSSE from 'vue-sse';

export default defineNuxtPlugin((nuxtApp) => {
  nuxtApp.vueApp.use(VueSSE);
});
