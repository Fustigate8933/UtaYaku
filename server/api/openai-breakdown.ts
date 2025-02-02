import { OpenAI } from "openai"

const client = new OpenAI()

export default defineEventHandler(async (event) => {
	const { history } = await readBody(event)

	console.log("Fetching break down from OpenAI...")

	const completion = await client.chat.completions.create({
		model: "gpt-4o",
		messages: history,
		stream: false
	})

	return completion.choices[0].message
})

