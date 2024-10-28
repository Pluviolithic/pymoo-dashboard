<template>
	<dialog ref="dialog" class="group pointer-events-none open:pointer-events-auto opacity-0 invisible open:visible open:opacity-100 grid transition-[opacity,backdrop-filter,visibility] fixed inset-0 backdrop:[transition:backdrop-filter_.5s_ease] backdrop-blur-sm bg-black/20 h-full w-full z-40 max-h-none max-w-none">
		<div class="h-full overflow-y-auto">
			<div class="motion-safe:animate-closeModal motion-safe:group-open:animate-openModal my-20 z-50 bg-white dark:bg-[#181a1b] text-black dark:text-[#e8e6e3] w-full max-w-[95vw] sm:max-w-lg data-[help=true]:max-w-screen-md rounded-lg shadow [--tw-shadow:0.3px_0.5px_0.7px_#0000001a,1.5px_2.9px_3.7px_-0.4px_#0000001a,2.7px_5.4px_6.8px_-0.7px_#0000001a,4.5px_8.9px_11.2px_-1.1px_#0000001a,7.1px_14.3px_18px_-1.4px_#0000001a,11.2px_22.3px_28.1px_-1.8px_#0000001a,17px_33.9px_42.7px_-2.1px_#0000001a,25px_50px_62.9px_-2.5px_#0000001a] [--tw-shadow-colored:0.3px_0.5px_0.7px_var(--tw-shadow-color),1.5px_2.9px_3.7px_-0.4px_var(--tw-shadow-color),2.7px_5.4px_6.8px_-0.7px_var(--tw-shadow-color),4.5px_8.9px_11.2px_-1.1px_var(--tw-shadow-color),7.1px_14.3px_18px_-1.4px_var(--tw-shadow-color),11.2px_22.3px_28.1px_-1.8px_var(--tw-shadow-color),17px_33.9px_42.7px_-2.1px_var(--tw-shadow-color),25px_50px_62.9px_-2.5px_var(--tw-shadow-color)] relative m-auto p-8">
				<h2 class="text-center block text-2xl font-bold my-4">
					{{ title }}
					<ImageContent :imageData="imageData" :title="title" />
				</h2>
			</div>
		</div>
		<form class="fixed inset-0 text-transparent" method="dialog">
			<button class="h-full w-full cursor-default" type="submit">Close</button>
		</form>
	</dialog>
	<Widget :title="title" @click="openModal" class="cursor-pointer peer-open:hidden [dialog[open]+&]:hidden">
		<ImageContent :imageData="imageData" :title="title" />
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