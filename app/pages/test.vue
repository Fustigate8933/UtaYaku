<template>
	<div>
		<div class="border-white border-2 resize-y p-4">
			<div class="border-white border-2 resize-y overflow-y-auto">
				asjkfjasdfkasdjfasdjkfj
			</div>
		</div>
	</div>
</template>

<script setup>

onMounted(async () => {
	const response = await fetch("/api/db/addBreakdown", {
		method: "POST",
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify({ musicId: "abc", allBreakdowns: [{"hello": "hello"}, {"goodbye": "goodbye"}], lyrics: ["abc", "def"], furigana: ["hi", "bye"], indices: [0, 1 ,2], timestamps: [[0, 1], [2, 3]], name: "piggy", artist: "piggy dad" })
	})
	const data = await response.text()
	console.log(data)
})
</script>
