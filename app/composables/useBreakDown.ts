export function useBreakDown(){
	async function getBreakDown(message: string, email: string, password: string, breakdown_type: string) {
		try {
			const response = await fetch("/api/breakdown", {
				method: "POST",
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({ req: message, email: email, password: password, breakdown_type: breakdown_type })
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

