<template>
	<div class="flex items-center flex-col justify-center h-full w-full gap-5 relative">
		<div class="max-w-5xl flex items-center flex-col justify-center h-full w-full gap-10 py-[4rem]">
			<div class="absolute inline-flex items-center cursor-pointer top-2 right-2" @click="useAiToggle">
				<input type="checkbox" value="" class="sr-only peer" :checked="useAi">
				<div class="relative w-11 h-6 bg-gray-200 rounded-full peer peer-focus:ring-2 peer-focus:ring-blue-300 dark:peer-focus:ring-blue-800 dark:bg-gray-700 peer-checked:after:translate-x-full rtl:peer-checked:after:-translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-0.5 after:start-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-gray-600 peer-checked:bg-blue-600"></div>
			</div>
			<div v-if="useAi" class="">
				<div class="w-full flex text-center justify-center items-center gap-3 mb-2">
					<h1 class="">HuggingChat Credentials:</h1>
					<div class="flex flex-col gap-1">
						<input v-model="huggingchatEmail" class="rounded-lg px-2 py-1 text-black" type="text" placeholder="Email" />
					</div>
					<div class="flex flex-col gap-1">
						<input v-model="huggingchatPassword" class="rounded-lg px-2 py-1 text-black" type="password" placeholder="Password" />
					</div>
					<button class="h-full rounded-lg hover:cursor-pointer border-2 border-gray-400 hover:border-white active:border-gray-400 px-2 py-1" @click="saveCredentials">{{ saved ? 'Saved' : 'Save' }}</button>
				</div>
				<ul class="ml-3 text-sm text-gray-400">
					<li>* Please provide your credentials from <span class="text-blue-300 underline"><a href="https://huggingface.co/chat/" target="_blank">HuggingChat</a></span>(free) as ai analysis requires it.</li>
					<li>* It's best to use a throwaway account for concerns of privacy and chat modification.</li>
				</ul>
			</div>
			<div class="w-full flex gap-10 text-center justify-center text-lg">
				<div class="flex flex-col gap-1">
					<label>曲 <span class="text-sm text-gray-400">(Song)</span></label>
					<input v-model="song_name" class="rounded-lg px-2 py-1 text-black" type="text" placeholder="曲名" @keyup.enter="getMetaData" />
				</div>
				<div class="flex flex-col gap-1">
					<label>アーティスト <span class="text-sm text-gray-400">(Artist)</span></label>
					<input v-model="artist_name" class="rounded-lg px-2 py-1 text-black" type="text" placeholder="アーティスト名" @keyup.enter="getMetaData" />
				</div>
				<div class="flex flex-col gap-1">
					<!-- <label class="invisible">Easter egg!</label> -->
					<label class="w-[100px]"><span class="text-sm text-gray-400">(Search)</span></label>
					<button class="h-full rounded-lg hover:cursor-pointer border-2 border-gray-400 hover:border-white active:border-gray-400" @click="getMetaData">検索</button>
				</div>
			</div>
			<div v-if="fetchingMetaData" class="flex items-center gap-3">
				<Shuriken size="25px" />
				<h1>Fetching {{ song_name }} {{ artist_name !== "" ? `by ${artist_name}` : "" }}</h1>
			</div>
			<div class="w-full flex flex-col gap-5 overflow-y-auto">
				<div v-if="noTracksFound">
					<h1 class="text-center">No tracks could be found.</h1>
				</div>
				<div
					v-else
					v-for="(candidate, i) in trackCandidates" 
					:key="i"
					class="border-2 rounded-xl border-[#4d4e51] p-4"
				>
					<NuxtLink :to="`/${candidate.id}`">
						<h1 class="font-bold">
							{{ candidate.trackName }}
						</h1>
						<h1 class="text-[#C5D3E8]">
							Artist: {{ candidate.artistName }}
						</h1>
						<h1 class="text-[#FFDDAE]">
							Album: {{ candidate.albumName }}
						</h1>
					</NuxtLink>
				</div>
			</div>
		</div>
	</div>
</template>

<script setup lang="ts">
const song_name = ref("")
const artist_name = ref("")
const trackCandidates = ref([])
const fetchingMetaData = ref(false)
const noTracksFound = ref(false)
const huggingchatEmail = ref("")
const huggingchatPassword = ref("")
const saved = ref(false)
const useAi = ref(false)

const getMetaData = async () => {
	trackCandidates.value = []
	fetchingMetaData.value = true
	const lyricsResponse = await fetch(`https://lrclib.net/api/search?track_name=${song_name.value}&artist_name=${artist_name.value}`)
	const lyricsResponseData = await lyricsResponse.json()

	if (lyricsResponseData.length === 0){
		noTracksFound.value = true
	} else {
		trackCandidates.value = lyricsResponseData
		noTracksFound.value = false
	}

	fetchingMetaData.value = false
}

const saveCredentials = () => {
	if (process.client) {
		localStorage.setItem("hugEmail", huggingchatEmail.value)
		localStorage.setItem("hugSecret", huggingchatPassword.value)
		saved.value = true
	}
}

const useAiToggle = () => {
	if (process.client) {
		useAi.value = !useAi.value
		localStorage.setItem("useAi", useAi.value)
	}
}

onMounted(() => {
	if (process.client) {
		const email = localStorage.getItem("hugEmail")
		const password = localStorage.getItem("hugSecret")
		const ai = localStorage.getItem("useAi")
		if (email !== null) {
			huggingchatEmail.value = email
		}
		if (password !== null) {
			huggingchatPassword.value = password
		}
		if (ai !== null) {
			if (ai === "true") {
				useAi.value = true
			} else {
				useAi.value = false
			}
		}
	}
})
</script>

