<template>
	<div id="app">
		<!-- Table widgets -->
		<Widget
			v-for="(tableContent, title) in tableWidgets"
			:key="title"
			:title="title"
		>
			<table>
				<tr
					v-for="(val, key) in tableContent"
					:key="key"
				>
					<th scope="row">
						{{ key }}
					</th>
					<td>
						{{ val }}
					</td>
				</tr>
			</table>
		</Widget>
		<form
			:action="WS_URL + '/pause'"
			method="post"
			@submit.prevent="pause"
		>
			<button
				id="pause-button"
				type="submit"
			>
				{{ buttonText }}
			</button>
		</form>

		<!-- Image widgets -->
		<ImageWidget
			v-for="(image, title) in imageData"
			:key="title"
			:title="title"
			:image-data="image"
		/>
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
			pausing: false,
			paused: false,
			imageData: {},
			tableWidgets: {},
			WS_URL: useRuntimeConfig().public.WS_URL,
		}
	},
	computed: {
		buttonText() {
			if (this.pausing)
				return 'Pausing...'
			if (this.paused)
				return 'Resume'
			return 'Pause'
		}
	},
	// Created hook 
	mounted() {
		const socket = io(this.WS_URL)
		socket.on('connect', this.connect)
		socket.on('initial_data', this.initialData)
		socket.on('update', this.update)
		socket.on('pausing', this.get_pausing)
		socket.on('pause', this.get_paused)
		socket.on('disconnect', this.disconnect)
	},
	methods: {
		async pause(event) {
			const form = event.currentTarget ?? event.target
			await fetch(form.action, { method: form.method })
		},
		connect() {
			console.log('Connected to server')
		},
		initialData(initial_data) {
			const start = performance.now()
			const data = JSON.parse(initial_data.msg)
			console.log('Time to parse initial data for a length of', data.length, ':', performance.now() - start)
			const tempImages = {}
			const startPopulate = performance.now()
			data.filter(({ title }) => title !== 'Overview').forEach(({ title, content }) => {
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
		},
		update(update) {
			console.log("I've got something!")
			const data = JSON.parse(update.msg)
			const { title, content } = data
			if (title === "Overview")
				return this.tableWidgets["Overview"] = content
			if (!this.imageData[title])
				this.imageData[title] = []
			this.imageData[title].push(content)
		},
		get_pausing(pausing) {
			this.pausing = JSON.parse(pausing.msg)
			console.log('Got pausing state of', this.pausing)
		},
		get_paused(paused) {
			this.pausing = false
			this.paused = JSON.parse(paused.msg)
			console.log('Got pause state of', this.paused)
		},
		disconnect() {
			console.log('Disconnected from server')
		}
	}
}
</script>