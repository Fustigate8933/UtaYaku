export default defineEventHandler(async (event) => {
	const { req, email, password, breakdown_type } = await readBody(event)

	console.log("Fetching break down from FastAPI...")

	const response = await fetch("http://localhost:8000/", {
		method: "POST",
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify({ query: req, email: email, password: password, breakdown_type: breakdown_type })
	})
	const data = await response.json()

	return data.breakdown
})

