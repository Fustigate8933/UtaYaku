import { serverSupabaseServiceRole } from '#supabase/server'

export default defineEventHandler(async (event) => {
  const client = serverSupabaseServiceRole(event)

  const { musicId } = await readBody(event)

  const { data, error } = await client
    .from("Song")
    .select("song_id")
    .eq("song_id", musicId)
    .single()

  if (error || !data) {
    return { result: false }
  }

  return { result: true }
})

