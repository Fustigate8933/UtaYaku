import { serverSupabaseServiceRole } from '#supabase/server'

export default defineEventHandler(async (event) => {
  const client = serverSupabaseServiceRole(event)

  // Read the musicId from the request body
  const { musicId } = await readBody(event)

  // Fetch data from the Song table
  const { data: songData, error: songError } = await client
    .from("Song")
    .select("name, artist")
    .eq("song_id", musicId)
    .single()

  // Fetch data from the Breakdown table
  const { data: breakdownData, error: breakdownError } = await client
    .from("Breakdown")
    .select("json_data")
    .eq("song_id", musicId)
    .single()

  // Fetch data from the Furigana table
  const { data: furiganaData, error: furiganaError } = await client
    .from("Furigana")
    .select("furigana")
    .eq("song_id", musicId)
    .single()

  // Fetch data from the Lyrics table
  const { data: lyricsData, error: lyricsError } = await client
    .from("Lyrics")
    .select("lyrics, indices, timestamps")
    .eq("song_id", musicId)
    .single()

  // Check for errors
  if (songError || breakdownError || furiganaError || lyricsError) {
    return {
      message: "Error occurred while fetching data",
      errors: {
        songError,
        breakdownError,
        furiganaError,
        lyricsError,
      },
    }
  }

  // Construct the combined response
  return {
    message: "Data fetched successfully",
    data: {
      name: songData.name,
      artist: songData.artist,
      allBreakdowns: breakdownData.json_data,
      furigana: furiganaData.furigana,
      lyrics: lyricsData.lyrics,
      indices: lyricsData.indices,
      timestamps: lyricsData.timestamps,
    },
  }
})

