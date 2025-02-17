<template>
	<div>
		<div class="w-full">
			<div id="embed-iframe"></div>
		</div>	</div>
</template>

<script setup lang="ts">
interface EmbedControllerType {
	addListener: (event: string, callback: (state: PlaybackState) => void) => void;
}
interface PlaybackState {
	data: { position: number };
}
interface IFrameAPIType {
	createController: (
		element: HTMLElement,
		options: { uri: string; width: string; height: number },
		callback: (EmbedController: EmbedControllerType) => void
	) => void
}

let embedController: EmbedControllerType | null = null
const initializeSpotifyEmbed = (trackUrl: string) => {
	window.onSpotifyIframeApiReady = (IframeAPI: IFrameAPIType) => {
		const element = document.getElementById("embed-iframe")
		if (!element) {
			console.error("Embed iframe element not found.")
			return
		}
		const options = {
			uri: trackUrl,
			width: "100%",
			height: 152
		}
		IframeAPI.createController(element, options, () => {})
	}
}

const foo = async () => {
	const embeddingResponse = await fetch("/api/musicapi", {
		method: "POST",
		headers: {
			'Content-Type': 'application/json',
		},
		body: JSON.stringify({ song_name: "Insomnia", artist_name: "Eve" })
	})
	console.log("neigh")
	const embeddingResponseData = await embeddingResponse.json()
	console.log(embeddingResponseData)
}

onMounted(async () => {
	initializeSpotifyEmbed("https://open.spotify.com/track/52KxsRBZj7Ip9HdxgvEQbO")
	await foo()
})
</script>
