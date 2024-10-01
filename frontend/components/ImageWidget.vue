<template>
	<Widget :title="title" v-bind:id="'plot-wrapper-' + slugify(title)" :optionalClasses="isEnlarged ? 'fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[calc(90vw-2rem)] h-[calc(90vh-2rem)] z-50' : ''">
		<img v-if="imageData && imageData.length > 0" @click="toggleEnlarge"
			v-bind:src="'data:image/gif; base64,' + imageData[index ?? imageData.length - 1]"
			v-bind:id="'graph-image-' + slugify(title)" v-bind:alt="title" class="w-full" />
		<input class="w-full" type="range" :min="0" :max="imageData.length - 1" step="1" :value="currentIndex"
			@input="updateIndex($event.target.value)" />
	</Widget>
</template>
<script>
	import Widget from './Widget.vue'
	export default {
		name: 'ImageWidget',
		props: {
			imageData: {
				type: Object,
				required: true
			},
			title: {
				type: String,
				required: true
			},
		},
		methods: {
			slugify(str) {
				return str.toLowerCase().trim().replace(/[^\w\s-]/g, '').replace(/[\s_-]+/g, '-').replace(/(?:^-+)|(?:-+$)/g, '')
			},
			toggleEnlarge() {
				this.isEnlarged = !this.isEnlarged
			},
			updateIndex(value) {
				this.index = value
			}
		},
		data() {
			return {
				index: null,
				isEnlarged: false
			}
		},
		computed: {
			currentIndex() {
				return this.index ?? this.imageData.length - 1
			}
		}
	}
</script>