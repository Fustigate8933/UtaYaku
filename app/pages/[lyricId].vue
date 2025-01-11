<template>
	<div class="flex items-center flex-col justify-center h-full w-full gap-5">
		<div class="max-w-4xl flex items-center flex-col justify-center h-full w-full gap-5 py-[4rem]">
			<div class="flex gap-3 items-baseline border-white border-b"> <h1 class="text-5xl text-yellow-100">{{song_name}}</h1>
				<h1 class="text-xl text-orange-200">({{artist_name}})</h1>
			</div>
			<div class="w-full h-40 p-4 overflow-y-auto border-[#4d4e51] border-2 rounded-xl resize-y flex-shrink-0 max-h-96 relative">
				<div v-if="generatingBreakdowns">
					<div class="flex justify-between mb-2">
						<h1 class="bg-gradient-to-r from-gray-200 via-gray-400 to-gray-50 inline-block text-transparent bg-clip-text">Generating breakdowns (this may take up to 3 minutes, do not refresh the page) ...</h1>
						<h1 class="text-white">{{progress}}%</h1>
					</div>
					<div class="w-full rounded-full h-2 bg-gray-700">
						<div class="bg-gray-300 h-2 rounded-full" :style="{'width': `${progress}%`}"></div>
					</div>
				</div>
				<div v-else>
					<button 
						class="absolute border-2 border-gray-400 hover:cursor-pointer rounded-lg px-2 text-gray-500 hover:text-gray-400 top-2 right-2 active:text-gray-500"
						@click="regenerateBreakdowns"
					>
						Regenerate
					</button>
					<h1 v-for="(key, i) in phrases" :key="i">
						<span class="text-[#bfe3b4]">{{ key }}</span>: {{ breakdown[key] }}
					</h1>
					<h1>
						<span class="text-orange-200">Translation</span>: {{ translation }}
					</h1>
				</div>
			</div>
			<div v-if="fetchedLyrics" class="flex flex-col text-[#F5F5F5bb] text-2xl overflow-y-auto gap-3 w-full p-4">
				<p
					v-for="(lyric_line, i) in lyrics"
					class="cursor-pointer"
					:class="{ 'text-yellow-100 font-bold': isCurLyric(lyricsIndices[i]) }"
					:id="lyricsIndices[i]"
					:key="i"
					@click="handleLineClick(lyricsIndices[i])"
				>
					{{ lyric_line === "" ? "♪" : lyric_line }}
				</p>
			</div>
			<div v-else>
				<div class="flex items-center gap-3">
					<Shuriken size="25px" />
					<h1 class="text-white">Fetching lyrics</h1>
				</div>
			</div>
			<div class="w-full" :class="embedReady ? '' : 'invisible'">
				<div id="embed-iframe"></div>
			</div>
			<div class="flex items-center gap-3" :class="embedReady ? 'hidden' : ''">
				<Shuriken size="25px" />
				<h1 class="text-white">Fetching lyrics</h1>
			</div>
		</div>
	</div>
</template>

<script setup lang="ts">
const route = useRoute()
const lyricId = route.params.lyricId

import removeMd from 'remove-markdown'

const lyrics = ref([])
const lyricsIndices = ref([])
const externalId = ref("")
const timestamps = ref([]) // in pairs format [start, end]
const playbackTime = ref(0)
const breakdown = ref({"Special message": "Click on a lyric to show breakdown!"})
const phrases = ref(["Special message"])
const translation = ref("Click on a lyric to show translation!")
const allBreakdowns = ref([])

const generatingBreakdowns = ref(false)
const batchesNeeded = ref(0)
const batchCount = ref(0)
const progress = ref(0)

const fetchedLyrics = ref(false)
const fetchedBreakdowns = ref(false)
const embedReady = ref(false)

const { getBreakDown } = useBreakDown()

const song_name = ref("Fetching song name")
const artist_name = ref("Fetching artist name")

const offset = ref(1)

function timestampToMS(timestamp: string){
	const [minutes, seconds, milliseconds] = timestamp.slice(1, -1).split(/[:.]/).map(Number)
	let ans
	if (milliseconds! >= 50){
		ans = (minutes! * 60) + seconds!
	} else {
		ans = (minutes! * 60) + seconds!
	}
	return ans
}

const filterTimestamps = (rawSynced: Array<string>) => {
	const matches = rawSynced.map(line => line.match(/\[\d{2}:\d{2}\.\d{2}\]/)![0]).map(timestamp => timestampToMS(timestamp))
	const l = matches.length
	let timeStampPairs = new Array<Array<number>>
	for (let i = 0; i < l - 1; i++){
		if (rawSynced[i]!.length > 11){ // not empty
			timeStampPairs.push([matches[i]!, matches[i + 1]!])
		}
	}
	timeStampPairs.push([matches[l - 1]!, matches[l - 1]! + 5])
	return timeStampPairs
}

const regenerateBreakdowns = async () => {
	const deleteBreakdownResult = await fetch("/api/deleteBreakdown", {
		method: "POST",
		headers: {
			'Content-Type': 'application/json',
		},
		body: JSON.stringify({ musicId: externalId.value })
	})
	const deleteBreakdownResultData = await deleteBreakdownResult.json()
	console.log(deleteBreakdownResultData.message)

	reloadNuxtApp()
}

const fetchMusicData = async () => {
	const lyricsResponse = await fetch(`https://lrclib.net/api/get/${lyricId}`)
	if (!lyricsResponse.ok) {
		throw new Error(`No song with id ${lyricId} could be found.`)
	}

	const lyricsData = await lyricsResponse.json()
	if (lyricsData.length === 0) {
		throw new Error(`No song with id ${lyricId} could be found.`)
	}

	song_name.value = lyricsData.trackName
	artist_name.value = lyricsData.artistName

	const rawLyrics = lyricsData.plainLyrics.split("\n")
	const rawSynced = lyricsData.syncedLyrics.split("\n").slice(0, -1)
	timestamps.value = filterTimestamps(rawSynced)
	const l = rawLyrics.length
	let indices = new Array<number>
	let j = 0
	for (let i = 0; i < l; i++){
		if (rawLyrics[i] !== ""){
			indices.push(j)
			j++
		} else {
			indices.push(-1)
		}
	}
	lyrics.value = rawLyrics
	lyricsIndices.value = indices
	fetchedLyrics.value = true

	const embeddingResponse = await fetch("/api/musicapi", {
		method: "POST",
		headers: {
			'Content-Type': 'application/json',
		},
		body: JSON.stringify({ song_name: song_name.value, artist_name: artist_name.value })
	})
	const embeddingResponseData = await embeddingResponse.json()
	const trackUrl = embeddingResponseData.url
	externalId.value = embeddingResponseData.externalId

	try {
		initializeSpotifyEmbed(trackUrl)
	} catch (error) {
		if (error instanceof Error) {
			console.error(error.message)
		} else{
			console.error("Unknown error: ", error)
		}
	}

	try {
		const breakdownExistsResult = await fetch("/api/needBreakdown", {
			method: "POST",
			headers: {
				'Content-Type': 'application/json',
			},
			body: JSON.stringify({ musicId: externalId.value })
		})
		const breakdownExistsData = await breakdownExistsResult.json()
		const breakdownExists = breakdownExistsData.result

		if (!breakdownExists) {
			console.log("Breakdown doesn't exist, fetching from backend.")
			breakdown.value = {"Special message": "This song is new in the system, generating breakdown."}
			phrases.value = ["Special message"]
			translation.value = "New song detected, generating breakdown."
			
			generatingBreakdowns.value = true

			const batchSize = 7
			batchesNeeded.value = Math.ceil(l / batchSize)
			let buffer = ""
			let bufferCount = 0
			for (let i = 0; i < l; i++){
				if (rawLyrics[i] !== ""){
					buffer += rawLyrics[i] + "\n"
					bufferCount++
					if (bufferCount === batchSize){
						if (buffer.endsWith("\n")){
							buffer = buffer.slice(0, -1)
						}

						console.log(`Processing batch ${batchCount.value}`)
						const result = await getBreakDown(buffer)

						for (let j = 0; j < batchSize; j++){
							allBreakdowns.value.push(result[j])
						}

						buffer = ""
						bufferCount = 0
						batchCount.value += 1
						progress.value = Math.floor(batchCount.value / batchesNeeded.value * 100)
						console.log("progress: ", progress.value)
					}
				}
			}

			if (bufferCount > 0){
				if (buffer.endsWith("\n")){
					buffer = buffer.slice(0, -1)
				}
				console.log("Processing last batch")
				const result = await getBreakDown(buffer)

				for (let j = 0; j < bufferCount; j++){
					allBreakdowns.value.push(result[j])
				}

				batchCount.value += 1
				progress.value = Math.floor(batchCount.value / batchesNeeded.value * 100)
			}

			// store breakdowns in to the database to prevent repeated future model queries
			const addBreakdownResult = await fetch("/api/addBreakdown", {
				method: "POST",
				headers: {
					'Content-Type': 'application/json',
				},
				body: JSON.stringify({ allBreakdowns: allBreakdowns.value, musicId: embeddingResponseData.externalId })
			})
			const addBreakdownResultData = await addBreakdownResult.json()
			console.log(addBreakdownResultData.message)

			breakdown.value = {"Special message": "Generation complete. Click on a lyric to view breakdown."}
			phrases.value = ["Special message"]
			translation.value = "Generation complete. Click on a lyric to show translation."
			
			generatingBreakdowns.value = false
		} else {
			console.log("Breakdowns already exists, fetching from database...")
			const fetchedBreakdownResult = await fetch("/api/getBreakdown", {
				method: "POST",
				headers: {
					'Content-Type': 'application/json',
				},
				body: JSON.stringify({ musicId: embeddingResponseData.externalId })
			})
			const fetchedBreakdownData = await fetchedBreakdownResult.json()
			console.log(fetchedBreakdownData.breakdowns)
			allBreakdowns.value = fetchedBreakdownData.breakdowns
		}
	}catch (error) {
		console.error("Error fetching breakdown: \n", error)
	}
}

interface IFrameAPIType {
	createController: (
		element: HTMLElement,
		options: { uri: string; width: string; height: number },
		callback: (EmbedController: EmbedControllerType) => void
	) => void
}

interface EmbedControllerType {
	addListener: (event: string, callback: (state: PlaybackState) => void) => void;
}

interface PlaybackState {
	data: { position: number };
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
		const callback = (EmbedController: EmbedControllerType) => {
			embedController = EmbedController
			EmbedController.addListener("playback_update", (state) => {
				playbackTime.value = state.data.position
			})
			EmbedController.addListener('ready', () => {
				console.log("embedder ready")
				embedReady.value = true
			});
		}
		IframeAPI.createController(element, options, callback)
	}
}

const handleLineClick = (i: number) => {
	const cur = allBreakdowns.value[i]
	if (cur !== null){
		breakdown.value = cur
		phrases.value = Object.keys(cur).filter(key => key !== "translation")
		translation.value = cur["translation"]
	} else {
		breakdown.value = {"Special message": "No breakdown found for this line"}
		phrases.value = ["Special message"]
		translation.value = "No translation found"
	}

	const newTime = timestamps.value[i][0]
	if (embedController) {
		embedController.seek(newTime + offset.value)
	} else {
		console.error("Embed Controller not initialized")
	}
}

const isCurLyric = (i: number) => {
	const playbackInSeconds = Math.floor(playbackTime.value / 1000)
	return i !== -1 && (timestamps.value[i][0] <= playbackInSeconds - offset.value) && (playbackInSeconds - offset.value < timestamps.value[i][1])
}

watch(playbackTime, (newPlaybackTime:number , oldPlaybackTime: number) => {
	const playbackInSeconds = Math.floor(newPlaybackTime / 1000)
	let currentIndex = timestamps.value.findIndex(
		([start, end]: [number, number]) => start <= playbackInSeconds - offset.value && playbackInSeconds - offset.value < end
	)

	if (currentIndex !== -1) {
		const cur = allBreakdowns.value[currentIndex]
		if (cur) {
			breakdown.value = cur
			phrases.value = Object.keys(cur).filter((key) => key !== "translation")
			translation.value = cur["translation"]
		} else {
			breakdown.value = { "Special message": "No breakdown found for this line" }
			phrases.value = ["Special message"]
			translation.value = "No translation found"
		}

		document.getElementById(`${currentIndex}`)!.scrollIntoView({ behavior: "smooth", block: "center" })
	} else {
			breakdown.value = { "Music": "🎶" }
			phrases.value = ["Music"]
			translation.value = "🎶"
	}
})

onMounted(() => {
	fetchMusicData()
})
</script>


