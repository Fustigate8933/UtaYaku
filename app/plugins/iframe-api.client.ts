export default defineNuxtPlugin(() => {
  return new Promise<void>((resolve) => {
    if (import.meta.client) {
      const script = document.createElement('script')
      script.src = 'https://open.spotify.com/embed/iframe-api/v1'
      script.async = true
      document.body.appendChild(script)

      script.onload = () => {
        resolve()
      }
    } else {
      resolve()
    }
  })
})

