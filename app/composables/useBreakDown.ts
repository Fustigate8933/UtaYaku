export function useBreakDown(){
	async function getBreakDown(message: string) {
		try {
			const response = await fetch("/api/breakdown", {
				method: "POST",
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({ req: message})
			})

			const data = await response.json()

			console.log(data)
		
			return data
		} catch (error) {
			console.error("Breakdown error: ", error)
			return
		}
	}

	return {
		getBreakDown
	}
}

