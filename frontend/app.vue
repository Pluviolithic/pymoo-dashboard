<template>
	<div id="app">
		<!-- Table widgets -->
		<Widget v-for="(tableContent, title) in tableWidgets" :title="title">
			<table>
				<tr v-for="(val, key) in tableContent">
					<th scope="row">{{ key }}</th>
					<td>{{ val }}</td>
				</tr>
			</table>
		</Widget>
		<form @submit.prevent="pause" action="http://localhost:5000/pause" method="post">
			<button id="pause-button" type="submit">{{ buttonText }}</button>
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
			pausing: false,
			paused: false,
			imageData: {},
			tableWidgets: {},
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
	methods: {
		async pause(event) {
			const form = event.currentTarget ?? event.target
			await fetch(form.action, { method: form.method })
		}
	},
	// Created hook 
	mounted() {
		const socket = io('https://5000.joshuastock.net')
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
		socket.on('pausing', (pausing) => {
			this.pausing = JSON.parse(pausing.msg)
			console.log('Got pausing state of', this.pausing)
		})
		socket.on('pause', (paused) => {
			this.pausing = false
			this.paused = JSON.parse(paused.msg)
			console.log('Got pause state of', this.paused)
		})
		socket.on('disconnect', () => {
			console.log('Disconnected from server')
		})
	}
}
</script>