export function useBreakDown(){
	async function getBreakDown(message: string, email: string, password: string) {
		try {
			const response = await fetch("/api/breakdown", {
				method: "POST",
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({ req: message, email: email, password: password })
			})
			const data = await response.text()
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

