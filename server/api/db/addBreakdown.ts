import { serverSupabaseServiceRole } from '#supabase/server'

export default defineEventHandler(async (event) => {
	const client = serverSupabaseServiceRole(event)

	const { musicId, allBreakdowns, lyrics, furigana, indices, timestamps, name, artist } = await readBody(event)
		
	const { data: songRes, error: songError } = await client
		.from("Song")
		.insert({ song_id: musicId, name: name, artist: artist })
	const { data: breakdownRes, error: breakdownError } = await client
		.from("Breakdown")
		.insert({ song_id: musicId, json_data: allBreakdowns })
	const { data: furiganaRes, error: furiganaError } = await client
		.from("Furigana")
		.insert({ song_id: musicId, furigana: furigana })
	const { data: lyricsRes, error: lyricsError } = await client
		.from("Lyrics")
		.insert({ song_id: musicId, lyrics: lyrics, indices: indices, timestamps: timestamps })

	if (songError || breakdownError || furiganaError || lyricsError) {
		return { 
			message: "error occured while deleting breakdown",  
      errors: {
        songError,
        breakdownError,
        furiganaError,
        lyricsError,
      }
		}
	} else {
		return { message: "data added successfully" }
	}
})
