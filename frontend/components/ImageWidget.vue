<template>
	<dialog ref="dialog">
		<div>
			<div>
				<h2>
					{{ title }}
					<ImageContent
						:image-data="imageData"
						:title="title"
					/>
				</h2>
			</div>
		</div>
		<form method="dialog">
			<button type="submit">
				Close
			</button>
		</form>
	</dialog>
	<Widget
		class="image-widget"
		:title="title"
		@click="openModal"
	>
		<ImageContent
			:imageData="imageData"
			:title="title"
		/>
	</Widget>
</template>
<script>
import Widget from './Widget.vue'
import ImageContent from './ImageContent.vue'
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
		openModal(e) {
			console.log('is open', this.$refs.dialog.open)
			const whitelist = ['button', 'input', 'a', 'svg']
			if (whitelist.includes((e.target ?? e.currentTarget).localName))
				return
			this.$refs.dialog.showModal()
		}
	}
}
</script>