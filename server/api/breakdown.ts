export default defineEventHandler(async (event) => {
	const { req } = await readBody(event)

	console.log("Fetching break down from hugchat...")

	const response = await fetch("http://localhost:8000/", {
		method: "POST",
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify({ query: req })
	})
	const data = await response.json()

	return data.breakdown
})

