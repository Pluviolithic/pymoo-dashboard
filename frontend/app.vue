<template>
	<div id="app" class="max-w-[calc(100%-5rem]) p-20 m-auto text-black dark:text-[#e8e6e3] bg-[#e8e8e8] dark:bg-[#25282a]">
		<!-- Table widgets -->
		<Widget v-for="(tableContent, title) in tableWidgets" :title="title">
			<table class="text-xl">
				<tr v-for="(val, key) in tableContent">
					<th scope="row" class="font-normal text-left border border-black dark:border-[#8c8273] border-collapse p-2">{{ key }}</th>
					<td class="border border-black dark:border-[#8c8273] border-collapse p-2">{{ val }}</td>
				</tr>
			</table>
		</Widget>

		<!-- Image widgets -->
		<ImageWidget v-for="(imageData, title) in imageData" :title="title" :imageData="imageData" :key="title" />
	</div>
</template>

<script>
import Widget from './components/Widget.vue'
import ImageWidget from './components/ImageWidget.vue'

import { createApp } from 'vue'

export default {
	data() {
		return {
			imageData: {},
			tableWidgets: {},
		}
	},
	// Created hook 
	mounted() {
		this.$sse.create('/listen')
			.on('message', (message) => {
				console.log("I've got something!")
				const data = JSON.parse(message)

				const title = data.title

				if (title === "Overview")
					return this.tableWidgets["Overview"] = data.content

				if (!this.imageData[title])
					this.imageData[title] = []

				this.imageData[title].push(data.content)
			})
			.on('error', (err) => console.error('Failed to parse or lost connection:', err))
			.connect()
			.catch((err) => console.error('Failed make initial connection:', err));
	}
}
</script>