<template>
	<div id="widget">
		<h2>
			{{ title }}
		</h2>
		<slot />
	</div>
</template>

<script>
export default {
	name: 'Widget',
	props: {
		title: {
			type: String,
			required: true
		}
	}
}
</script>