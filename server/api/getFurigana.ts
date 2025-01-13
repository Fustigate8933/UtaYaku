import Kuroshiro from "kuroshiro"
import KuromojiAnalyzer from "kuroshiro-analyzer-kuromoji"

export default defineEventHandler(async (event) => {
	const { text } = await readBody(event)
	const kuroshiro = new Kuroshiro()
	await kuroshiro.init(new KuromojiAnalyzer())
	const result = await kuroshiro.convert(text, {to: "hiragana", mode: "furigana"})
	console.log("furigana success")
	
	return result
})
