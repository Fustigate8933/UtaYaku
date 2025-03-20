export default defineEventHandler(async (event) => {
	const { req, email, password, breakdown_type } = await readBody(event)

	console.log("Fetching break down from backend...")
	
	const uri = "http://localhost:8000"
	// const uri = "https://y36chang.csclub.cloud/"
	const response = await fetch(uri, {
		method: "POST",
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify({ query: req, email: email, password: password, breakdown_type: breakdown_type })
	})
	const data = await response.json()

	return data.breakdown
})

