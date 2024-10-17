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
		<form @submit.prevent="pause" action="http://localhost:5000/pause" method="post">
			<button type="submit" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">{{ buttonText }}</button>
		</form>

		<!-- Image widgets -->
		<ImageWidget v-for="(imageData, title) in imageData" :title="title" :imageData="imageData" :key="title" />
	</div>
</template>

<script>
import Widget from './components/Widget.vue'
import ImageWidget from './components/ImageWidget.vue'

import { createApp } from 'vue'
import { io } from 'socket.io-client'

export default {
	data() {
		return {
			paused: false,
			imageData: {},
			tableWidgets: {},
		}
	},
	computed: {
		buttonText() {
			return this.paused ? 'Resume' : 'Pause'
		}
	},
	methods: {
		async pause(event) {
			const form = event.currentTarget ?? event.target
			await fetch(form.action, { method: form.method })
		}
	},
	// Created hook 
	mounted() {
		const socket = io('http://localhost:5000')
		socket.on('connect', () => {
			console.log('Connected to server')
		})
		socket.on('initial_data', (initial_data) => {
			const start = performance.now()
			const data = JSON.parse(initial_data.msg)
			console.log('Time to parse initial data for a length of', data.length, ':', performance.now() - start)
			const tempImages = {}
			const startPopulate = performance.now()
			data.filter(({ title }) => title !== 'Overview').forEach(({title, content}) => {
				if (!tempImages[title])
					tempImages[title] = []
				tempImages[title].push(content)
			})
			console.log('Time to populate initial data:', performance.now() - startPopulate)
			const startOverview = performance.now()
			this.tableWidgets['Overview'] = data.findLast(entry => entry.title === 'Overview')?.content
			console.log('Time to populate overview:', performance.now() - startOverview)
			const startImages = performance.now()
			Object.entries(tempImages).forEach(entry => {
				if (!this.imageData[entry[0]])
					this.imageData[entry[0]] = []
				this.imageData[entry[0]].unshift(...entry[1])
			})
			console.log('Time to populate images:', performance.now() - startImages)
		})
		socket.on('update', (update) => {
			console.log("I've got something!")
			const data = JSON.parse(update.msg)
			const { title, content } = data
			if (title === "Overview")
				return this.tableWidgets["Overview"] = content
			if (!this.imageData[title])
				this.imageData[title] = []
			this.imageData[title].push(content)
		})
		socket.on('pause', (paused) => {
			this.paused = JSON.parse(paused.msg)
			console.log('Got pause state of', this.paused)
		})
		socket.on('disconnect', () => {
			console.log('Disconnected from server')
		})
	}
}
</script>