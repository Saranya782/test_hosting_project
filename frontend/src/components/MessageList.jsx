import './MessageList.css'

function MessageList({ messages, loading, error, onRefresh }) {
  const formatDate = (dateString) => {
    const date = new Date(dateString)
    return date.toLocaleString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    })
  }

  if (loading) {
    return (
      <div className="message-list-container">
        <div className="message-list-header">
          <h2>Submitted Messages</h2>
          <button onClick={onRefresh} className="refresh-button" disabled>
            Refresh
          </button>
        </div>
        <div className="loading">Loading messages...</div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="message-list-container">
        <div className="message-list-header">
          <h2>Submitted Messages</h2>
          <button onClick={onRefresh} className="refresh-button">
            Refresh
          </button>
        </div>
        <div className="error-message">{error}</div>
      </div>
    )
  }

  return (
    <div className="message-list-container">
      <div className="message-list-header">
        <h2>Submitted Messages</h2>
        <button onClick={onRefresh} className="refresh-button">
          Refresh
        </button>
      </div>

      {messages.length === 0 ? (
        <div className="empty-state">
          <p>No messages yet. Be the first to submit one!</p>
        </div>
      ) : (
        <div className="messages-list">
          {messages.map((message) => (
            <div key={message.id} className="message-card">
              <div className="message-header">
                <div className="message-author">
                  <strong>{message.name}</strong>
                  <span className="message-email">{message.email}</span>
                </div>
                <span className="message-date">{formatDate(message.created_at)}</span>
              </div>
              <div className="message-content">{message.message}</div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default MessageList

