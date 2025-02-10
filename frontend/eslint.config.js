import pluginVue from 'eslint-plugin-vue'
export default [
	...pluginVue.configs['flat/recommended'],
	{
		files: ['**/*.{js,ts,vue}'],
		ignores: ['.nuxt/**/*'],
		rules: {
			'vue/html-indent': ['error', 'tab'],
		}
	}
]