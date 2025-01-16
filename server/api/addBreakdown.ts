export default defineEventHandler(async (event) => {
	const { allBreakdowns, musicId, lyrics, furigana } = await readBody(event)

	console.log("Storing breakdowns for ", musicId)

	try {
		const db = useDatabase("breakdowns")
		
		// Creation of table if it does not exist
		await db.sql`
			CREATE TABLE IF NOT EXISTS Song (
			song_id TEXT PRIMARY KEY,
			name TEXT,
			artist TEXT
		)`

		await db.sql`
			CREATE TABLE IF NOT EXISTS Breakdowns (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			song_id INTEGER NOT NULL,
			json_data TEXT NOT NULL,
			FOREIGN KEY (song_id) REFERENCES Song(song_id)
		)`

		await db.sql`
			CREATE TABLE IF NOT EXISTS Lyrics (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				song_id INTEGER NOT NULL,
				lyrics TEXT NOT NULL,
				FOREIGN KEY (song_id) REFERENCES Song(song_id)
			)`

		await db.sql`
			CREATE TABLE IF NOT EXISTS Furigana (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				song_id INTEGER NOT NULL,
				furigana TEXT NOT NULL,
				FOREIGN KEY (song_id) REFERENCES Song(song_id)
			)`
		
		// storing data to database
		await db.sql`
			INSERT INTO Song (song_id)
			VALUES (${musicId})
		`

		for (const breakdown of allBreakdowns) {
			await db.sql`
				INSERT INTO Breakdowns (song_id, json_data)
				VALUES (${musicId}, ${JSON.stringify(breakdown)})
			`
		}

		await db.sql`
			INSERT INTO Lyrics (song_id, lyrics)
			VALUES (${musicId}, ${lyrics})
		`

		await db.sql`
			INSERT INTO Furigana (song_id, furigana)
			VALUES (${musicId}, ${furigana})
		`

		return { message: "Breakdowns added successfully" }
	} catch (error) {
		console.error(error)
		return { message: "Add breakdown operation failed" }
	}
})
