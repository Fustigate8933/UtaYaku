<template>
	<div class="flex items-center flex-col justify-center h-full w-full gap-5">
		<div class="max-w-4xl flex items-center flex-col h-full w-full gap-4 py-[3rem]">
			<NuxtLink to="/" class="self-start border-2 border-gray-400 hover:cursor-pointer rounded-lg px-2 text-lg text-gray-400 hover:text-white active:text-gray-500">
				Home
			</NuxtLink>
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
						<div class="animate-pulse bg-gray-300 h-2 rounded-full" :style="{'width': `${progress}%`}"></div>
					</div>
				</div>
				<div v-else>
					<div v-if="useAi">
						<div class="absolute right-2 top-2 flex gap-1">
							<button
								class="border-2 border-gray-400 hover:cursor-pointer rounded-lg px-2 text-gray-500 hover:text-gray-400 active:text-gray-500"
								@click="regenerateBreakdowns"
							>
								Regenerate
							</button>
							<button 
								class="border-2 border-gray-400 hover:cursor-pointer rounded-lg px-2 text-gray-500 hover:text-gray-400 active:text-gray-500"
								@click="() => {expand = !expand}"
							>
								Expand
							</button>
						</div>
						<h1 v-for="(key, i) in phrases" :key="i">
							<span class="text-[#bfe3b4]">{{ key }}</span>: {{ breakdown[key] }}
						</h1>
						<h1>
							<span class="text-orange-200">Translation</span>: {{ translation }}
						</h1>
					</div>
					<div v-else class="flex flex-col gap-1">
						<div class="absolute right-2 top-2 flex gap-1">
							<button
								class="border-2 border-gray-400 hover:cursor-pointer rounded-lg px-2 text-gray-500 hover:text-gray-400 active:text-gray-500"
								@click="regenerateBreakdowns"
							>
								Regenerate
							</button>
							<button 
								class="border-2 border-gray-400 hover:cursor-pointer rounded-lg px-2 text-gray-500 hover:text-gray-400 active:text-gray-500"
								@click="() => {expand = !expand}"
							>
								Expand
							</button>
						</div>
						<div v-for="(key, i) in phrases" :key="i">
							<div v-for="(key2, j) in breakdown[i]" :key="j">
								<h1 class="text-[#bfe3b4]">{{ j }}</h1> <!-- main breakdown -->
								<div v-for="(key3, k) in breakdown[i][j]" :key="k">
									<ul>
										<li v-for="(key4, l) in key3" :key="l">
											<h1 v-if="Object.keys(breakdown[i][j]).length !== 1" class="pl-3">* {{ l }}</h1> <!-- breakdown component -->
											<ul>
												<li v-for="(key5, m) in key4" :key="m">
													<div v-if="m === 0" class="flex items-center pl-6 gap-2">
														<!-- <Icon name="icons8:angle-right" size="0.8rem" /> -->
														<Icon name="radix-icons:dot-filled" size="0.8rem" />
														<h1>
															{{ key5 }} <!-- component definition -->
														</h1>
													</div>
													<div v-if="expand && m !== 0" class="flex items-center pl-6 gap-2">
														<Icon name="radix-icons:dot-filled" size="0.8rem" />
														<h1>
															{{ key5 }} <!-- component definition -->
														</h1>
													</div>
												</li>
											</ul>
										</li>
									</ul>
								</div>
							</div>
						</div>
					</div>
				</div>
			</div>
			<div v-if="fetchedLyrics" class="overflow-y-auto w-full relative">
				<label class="absolute inline-flex items-center cursor-pointer top-2 right-4">
					<!-- <span class="ms-3 text-sm font-medium text-gray-900 dark:text-gray-300">Furigana</span> -->
					<input type="checkbox" value="" class="sr-only peer" :checked="furigana" @click="() => {furigana = !furigana}">
					<div class="relative w-11 h-6 bg-gray-200 rounded-full peer peer-focus:ring-2 peer-focus:ring-blue-300 dark:peer-focus:ring-blue-800 dark:bg-gray-700 peer-checked:after:translate-x-full rtl:peer-checked:after:-translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-0.5 after:start-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-gray-600 peer-checked:bg-blue-600"></div>
				</label>
				<div v-if="furigana" class="flex flex-col text-[#F5F5F5bb] text-2xl gap-3 p-4">
					<div
						v-for="(furiganaLine, i) in furiganalyzedLyrics"
						class="cursor-pointer"
						:class="{ 'text-yellow-100 font-bold': isCurLyric(lyricsIndices[i]) }"
						:id="lyricsIndices[i]"
						:key="i"
						@click="handleLineClick(lyricsIndices[i])"
					>
						<div v-if="furiganaLine === null">♪</div>
						<div class="flex items-baseline" v-html="furiganaLine"></div>
					</div>
				</div>
				<div v-else class="flex flex-col text-[#F5F5F5bb] text-2xl gap-3 p-4">
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
				<h1 class="text-white">Fetching embedded player</h1>
			</div>
		</div>
	</div>
</template>

<script setup lang="ts">
const route = useRoute()
const lyricId = route.params.lyricId
import removeMd from 'remove-markdown'

const expand = ref(false)
const furigana = ref(true)
const lyrics = ref([])
const furiganalyzedLyrics = ref([])
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

const useAi = ref(false)

const fetchedLyrics = ref(false)
const fetchedBreakdowns = ref(false)
const embedReady = ref(false)

const { getBreakDown } = useBreakDown()
const { getOpenAIBreakDown } = useOpenAIBreakDown()

const song_name = ref("Fetching song name")
const artist_name = ref("Fetching artist name")

const offset = ref(0)

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
	const deleteBreakdownResult = await fetch("/api/db/deleteBreakdown", {
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

const getFurigana = async (text: string) => {
	const response = await fetch("/api/getFurigana", {
		method: "POST",
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify({ text: text })
	})
	const data = await response.text()
	return data
}

const aiFetch = async (l: any, rawLyrics: any, embeddingResponseData: any) => {
	try {
		let email = ""
		let password = ""
		if (process.client) {
			const hugEmail = localStorage.getItem("hugEmail")
			if (hugEmail !== null){
				email = hugEmail
			}
			const hugPassword = localStorage.getItem("hugSecret")
			if (hugPassword !== null){
				password = hugPassword
			}
		}

		if (email === "" || password === "") {
			breakdown.value = {"Special message": "Your HuggingChat credentials were incorrect."}
			phrases.value = ["Special message"]
			translation.value = "Your HuggingChat credentials were incorrect."
		} else {
			console.log("Breakdown doesn't exist, fetching from backend.")
			breakdown.value = {"Special message": "This song is new in the system, generating breakdown."}
			phrases.value = ["Special message"]
			translation.value = "New song detected, generating breakdown."

			generatingBreakdowns.value = true

			const batchSize = 7
			batchesNeeded.value = Math.ceil(l / batchSize)
			let buffer = ""
			let bufferCount = 0
			let success = true // no errors during breakdown fetch
			for (let i = 0; i < l; i++){
				if (rawLyrics[i] !== ""){
					buffer += rawLyrics[i] + "\n"
					bufferCount++
					if (bufferCount === batchSize){
						if (buffer.endsWith("\n")){
							buffer = buffer.slice(0, -1)
						}

						console.log(`Processing batch ${batchCount.value}`)
						// const result = await getBreakDown(buffer, email, password, "huggingchat")
						let result = removeMd((await getOpenAIBreakDown(buffer)).content.replace(/\n\s+/g, "")).replace("`", "")
						if (result === "wrong username or password"){
							breakdown.value = {"Special message": "Your HuggingChat credentials were incorrect."}
							phrases.value = ["Special message"]
							translation.value = "Your HuggingChat credentials were incorrect."
							success = false
							break
						}

						const content = JSON.parse(result)

						for (let j = 0; j < batchSize; j++){
							allBreakdowns.value.push(content[j])
						}

						buffer = ""
						bufferCount = 0
						batchCount.value += 1
						progress.value = Math.floor(batchCount.value / batchesNeeded.value * 100)
						console.log("progress: ", progress.value)
					}
				}
			}

			if (success && bufferCount > 0){
				if (buffer.endsWith("\n")){
					buffer = buffer.slice(0, -1)
				}

				console.log(`Processing batch ${batchCount.value}`)
				// const result = await getBreakDown(buffer, email, password, "huggingchat")
				let result = removeMd((await getOpenAIBreakDown(buffer)).content.replace(/\n\s+/g, "")).replace("`", "")

				if (result === "wrong username or password"){
					breakdown.value = {"Special message": "Your HuggingChat credentials were incorrect."}
					phrases.value = ["Special message"]
					translation.value = "Your HuggingChat credentials were incorrect."
					success = false
				} else {
					const content = JSON.parse(result)

					for (let j = 0; j < batchSize; j++){
						allBreakdowns.value.push(content[j])
					}

					batchCount.value += 1
					progress.value = Math.floor(batchCount.value / batchesNeeded.value * 100)
				}
			}

			// store breakdowns in to the database 
			if (success){
				const addBreakdownResult = await fetch("/api/db/addBreakdown", {
					method: "POST",
					headers: {
						'Content-Type': 'application/json',
					}, // allBreakdowns, lyrics, furigana, indices, timestamps, name, artist
					body: JSON.stringify({ 
						allBreakdowns: allBreakdowns.value.map((breakdown) => JSON.stringify(breakdown)),
						musicId: embeddingResponseData.externalId,
						lyrics: lyrics.value, 
						furigana: furiganalyzedLyrics.value, 
						indices: lyricsIndices.value, 
						timestamps: timestamps.value, 
						name: song_name.value, 
						artist: artist_name.value 
					})
				})
				const addBreakdownResultData = await addBreakdownResult.json()
				console.log(addBreakdownResultData.message)

				breakdown.value = {"Special message": "Generation complete. Click on a lyric to view breakdown."}
				phrases.value = ["Special message"]
				translation.value = "Generation complete. Click on a lyric to show translation."
			}

			generatingBreakdowns.value = false
		}
	}catch (error) {
		console.error("Error fetching breakdown: \n", error)
		breakdown.value = {"Special message": "Generation failed. You can try regenerating it by pressing the button on the top right."}
		phrases.value = ["Special message"]
		translation.value = "Generation failure."
		generatingBreakdowns.value = false
	}
}

const ichiranFetch = async (l: any, rawLyrics: any, embeddingResponseData: any) => {
	console.log("Fetching with ichiran")

	breakdown.value = {"Special message": "This song is new in the system, generating breakdown."}
	phrases.value = ["Special message"]
	translation.value = "New song detected, generating breakdown."

	generatingBreakdowns.value = true

	let success = true // no errors during breakdown fetch
	for (let i = 0; i < l; i++){
		console.log("Raw lyrics", i, rawLyrics[i])
		if (rawLyrics[i] !== "" && rawLyrics[i] !== "♪"){
			const result = await getBreakDown(rawLyrics[i], "", "", "ichiran")
			breakdown.value = {"Special message": "Your HuggingChat credentials were incorrect."}
			phrases.value = ["Special message"]
			translation.value = "Your HuggingChat credentials were incorrect."
			
			const content = JSON.parse(result!)
			// console.log(rawLyrics[i], content)
			
			allBreakdowns.value.push(content)

			progress.value = Math.floor((i + 1) / l * 100)
			// console.log("progress: ", progress.value)
		}
	}
	// console.log("all breakdowns: ", allBreakdowns.value)

	if (success){
		const addBreakdownResult = await fetch("/api/db/addBreakdown", {
			method: "POST",
			headers: {
				'Content-Type': 'application/json',
			}, // allBreakdowns, lyrics, furigana, indices, timestamps, name, artist
			body: JSON.stringify({ 
				allBreakdowns: allBreakdowns.value.map((breakdown) => JSON.stringify(breakdown)),
				musicId: embeddingResponseData.externalId,
				lyrics: lyrics.value, 
				furigana: furiganalyzedLyrics.value, 
				indices: lyricsIndices.value, 
				timestamps: timestamps.value, 
				name: song_name.value, 
				artist: artist_name.value 
			})
		})
		const addBreakdownResultData = await addBreakdownResult.json()
		console.log(addBreakdownResultData.message)

		breakdown.value = {"Special message": "Generation complete. Click on a lyric to view breakdown."}
		phrases.value = ["Special message"]
		translation.value = "Generation complete. Click on a lyric to show translation."
	}

	generatingBreakdowns.value = false

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

	// get song metadata
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

	// check if song has already been process before
	const breakdownExistsResult = await fetch("/api/db/needBreakdown", {
		method: "POST",
		headers: {
			'Content-Type': 'application/json',
		},
		body: JSON.stringify({ musicId: externalId.value })
	})
	const breakdownExistsData = await breakdownExistsResult.json()
	const breakdownExists = breakdownExistsData.result

	if (breakdownExists) {
		console.log("Breakdowns already exists, fetching from database...")
		const fetchedBreakdownResult = await fetch("/api/db/getBreakdown", {
			method: "POST",
			headers: {
				'Content-Type': 'application/json',
			},
			body: JSON.stringify({ musicId: embeddingResponseData.externalId })
		})
		const fetchedBreakdownData = (await fetchedBreakdownResult.json()).data
		console.log(fetchedBreakdownData)
		allBreakdowns.value = fetchedBreakdownData.allBreakdowns.map((breakdown) => JSON.parse(breakdown))
		lyrics.value = fetchedBreakdownData.lyrics
		lyricsIndices.value = fetchedBreakdownData.indices.map(Number)
		timestamps.value = fetchedBreakdownData.timestamps.map((row) => row.map(Number))
		furiganalyzedLyrics.value = fetchedBreakdownData.furigana
		song_name.value = fetchedBreakdownData.name
		artist_name.value = fetchedBreakdownData.artist

		fetchedLyrics.value = true
		fetchedBreakdowns.value = true

		try {
			initializeSpotifyEmbed(trackUrl)
		} catch (error) {
			if (error instanceof Error) {
				console.error(error.message)
			} else{
				console.error("error during spotify embed initialization: ", error)
			}
		}

		embedReady.value = true

		return
	}

	// song hasn't been processed before
	const rawLyrics = lyricsData.plainLyrics.split("\n")
	const rawSynced = lyricsData.syncedLyrics.split("\n").slice(0, -1)
	timestamps.value = filterTimestamps(rawSynced)
	const l = rawLyrics.length
	let indices = new Array<number>
	let j = 0

	try {
		initializeSpotifyEmbed(trackUrl)
	} catch (error) {
		if (error instanceof Error) {
			console.error(error.message)
		} else{
			console.error("error during spotify embed initialization: ", error)
		}
	}

	const furiganaPromises = rawLyrics.map((lyric: string, i: number) => {
		if (lyric !== "") {
			indices.push(j)
			j++
			return getFurigana(lyric)
		} else {
			indices.push(-1)
			return Promise.resolve(null)
		}
	})

	try {
		const furiganaResults = await Promise.all(furiganaPromises)
		furiganalyzedLyrics.value = furiganaResults
	} catch (error) {
		console.error("Error fetching furigana:", error)
	}

	lyrics.value = rawLyrics
	lyricsIndices.value = indices
	fetchedLyrics.value = true

	if (useAi.value) {
		await aiFetch(l, rawLyrics, embeddingResponseData)
	} else {
		await ichiranFetch(l, rawLyrics, embeddingResponseData)
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


