import { useState, useEffect } from 'react'
import ContactForm from './components/ContactForm'
import MessageList from './components/MessageList'
import './App.css'

function App() {
  const [messages, setMessages] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  const fetchMessages = async () => {
    try {
      setLoading(true)
      setError(null)
      const data = await fetchMessagesFromAPI()
      setMessages(data)
    } catch (err) {
      setError('Failed to load messages. Please try again later.')
      console.error('Error fetching messages:', err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchMessages()
  }, [])

  const handleMessageSubmitted = () => {
    fetchMessages()
  }

  return (
    <div className="app">
      <div className="container">
        <header className="header">
          <h1>Contact Form App</h1>
          <p>Test your hosting platform deployment</p>
        </header>

        <div className="content">
          <div className="form-section">
            <ContactForm onMessageSubmitted={handleMessageSubmitted} />
          </div>

          <div className="messages-section">
            <MessageList 
              messages={messages} 
              loading={loading} 
              error={error}
              onRefresh={fetchMessages}
            />
          </div>
        </div>
      </div>
    </div>
  )
}

async function fetchMessagesFromAPI() {
  const backendUrl = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000'
  const response = await fetch(`${backendUrl}/api/messages`)
  
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`)
  }
  
  return await response.json()
}

export default App

