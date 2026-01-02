const getBackendUrl = () => {
  return import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000'
}

export const submitMessage = async (name, email, message) => {
  const backendUrl = getBackendUrl()
  const response = await fetch(`${backendUrl}/api/messages`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      name,
      email,
      message,
    }),
  })

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Unknown error' }))
    throw new Error(error.detail || `HTTP error! status: ${response.status}`)
  }

  return await response.json()
}

export const fetchMessages = async () => {
  const backendUrl = getBackendUrl()
  const response = await fetch(`${backendUrl}/api/messages`)

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`)
  }

  return await response.json()
}

