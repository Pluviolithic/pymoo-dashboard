<template>
	<Widget :title="title" :id="'plot-wrapper-' + slugify(title)"
		:optionalClasses="isEnlarged ? 'fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[calc(90vw-2rem)] h-[calc(90vh-2rem)] z-50 cursor-pointer' : 'cursor-pointer'">
		<img v-if="imageData && imageData.length > 0" @click="toggleEnlarge"
			v-bind:src="'data:image/gif; base64,' + imageData[currentIndex]"
			:id="'graph-image-' + slugify(title)" :alt="title" :class="isEnlarged ? 'h-[90%] mx-auto' : 'w-full'" />
		<input class="w-full" type="range" :min="0" :max="imageData.length - 1" step="1" v-bind:value="currentIndex"
			@input="updateIndex($event.target.value)" />
		<a v-bind:href="'data:image/gif; base64,' + imageData[currentIndex]" :download="'graph-image-' + slugify(title) + currentIndex + 1 + '.gif'">
			<span class="sr-only">Download image</span>
			<svg xmlns="http://www.w3.org/2000/svg" role="img" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-[1em] inline-block">
				<path stroke-linecap="round" stroke-linejoin="round" d="M3 16.5v2.25A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75V16.5M16.5 12 12 16.5m0 0L7.5 12m4.5 4.5V3" />
			</svg>
		</a>
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
			return str.toLowerCase().trim().replace(/[^\w\s-]|(?:^-+)|(?:-+$)/g, '').replace(/\s+/g, '-')
			// I believe these are equivalent but the above is less replace operations and is more clear what is being replaced. If we run into issues, revert back to this
			//return str.toLowerCase().trim().replace(/[^\w\s-]/g, '').replace(/[\s_-]+/g, '-').replace(/(?:^-+)|(?:-+$)/g, '')
		},
		toggleEnlarge() {
			this.isEnlarged = !this.isEnlarged
		},
		updateIndex(value) {
			if (value >= this.imageData.length - 1)
				return this.index = null
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