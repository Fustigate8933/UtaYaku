export default defineEventHandler(async (event) => {
	const { musicId } = await readBody(event)

	try {
		const db = useDatabase("breakdowns")

		const breakdowns = await db.sql`
			SELECT json_data
			FROM Breakdowns
			WHERE song_id = ${musicId}
		`

		const lyrics = await db.sql`
			SELECT lyrics 
			FROM Lyrics 
			WHERE song_id = ${musicId}
		`

		const furigana = await db.sql`
			SELECT furigana
			FROM Lyrics 
			WHERE song_id = ${musicId}
		`

		return { breakdowns: breakdowns.rows!.map(breakdown => JSON.parse(breakdown.json_data)), lyrics: lyrics, furigana: furigana }
	} catch (error) {
		console.error(error)
		return { message: "Add breakdown operation failed" }
	}
})


