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
	const response = await fetch("/api/db/getBreakdown", {
		method: "POST",
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify({ musicId: "6EzZn96uOc9JsVGNRpx06n" })
	})
	const data = await response.text()
	console.log(data)
})
</script>
