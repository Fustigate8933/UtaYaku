import { OpenAI } from "openai"

const client = new OpenAI({
  baseURL: "http://0.0.0.0:8000/v1",
})

export default defineEventHandler(async (event) => {
	const { history } = await readBody(event)

	console.log("Fetching break down from local llm...")

	const completion = await client.chat.completions.create({
		model: "Qwen/Qwen2.5-14B-Instruct",
		messages: history,
		stream: false
	})

	return completion.choices[0].message
})

