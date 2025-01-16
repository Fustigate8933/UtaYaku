import { serverSupabaseClient } from '#supabase/server'

export default defineEventHandler(async (event) => {
	const client = await serverSupabaseClient(event)
	const { musicId } = await readBody(event)
	
	const { error: lyricsError } = await client
    .from("Lyrics")
    .delete()
    .eq("song_id", musicId)

  const { error: furiganaError } = await client
    .from("Furigana")
    .delete()
    .eq("song_id", musicId)

  const { error: breakdownError } = await client
    .from("Breakdown")
    .delete()
    .eq("song_id", musicId)

  const { error: songError } = await client
    .from("Song")
    .delete()
    .eq("song_id", musicId)


	if (lyricsError || furiganaError || breakdownError || songError) {
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

