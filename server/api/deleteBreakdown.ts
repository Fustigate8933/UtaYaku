export default defineEventHandler(async (event) => {
	const { musicId } = await readBody(event)
	console.log("Attempting to delete ", musicId)

	try {
		const db = useDatabase("breakdowns")

		// await db.sql`
		// 	CREATE TABLE IF NOT EXISTS Song (
		// 	song_id TEXT PRIMARY KEY
		// )`
		//
		// await db.sql`
		// 	CREATE TABLE IF NOT EXISTS Breakdowns (
		// 	id INTEGER PRIMARY KEY AUTOINCREMENT,
		// 	song_id INTEGER NOT NULL,
		// 	json_data TEXT NOT NULL,
		// 	FOREIGN KEY (song_id) REFERENCES Song(song_id)
		// )`

		await db.sql`
			DELETE FROM Breakdowns
			WHERE song_id = ${musicId}
		`

		await db.sql`
			DELETE FROM Song
			WHERE song_id = ${musicId}
		`

		await db.sql`
			DELETE FROM Lyrics
			WHERE song_id = ${musicId}
		`

		await db.sql`
			DELETE FROM Furigana
			WHERE song_id = ${musicId}
		`
		
		console.log("Deletion successful.")
		return { message: "Song deleted successfully" }
	} catch (error) {
		console.log("Deletion failed.")
		console.error(error)
		return { message: "Song deletion failed" }
	}
})

