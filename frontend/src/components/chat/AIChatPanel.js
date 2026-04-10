'use client';

import { useState, useRef, useEffect } from 'react';
import api from '@/lib/api';

export default function AIChatPanel({ show, onToggle, datasetId, hasData }) {
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: 'Hi! I\'m your SmartPredict assistant. Upload some data and ask me anything about it — like "What are my total sales?" or "What trends do you see?"',
    },
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [suggestions, setSuggestions] = useState([
    'What are the main trends?',
    'Are there any risks?',
    'What should I focus on?',
  ]);
  const messagesEndRef = useRef(null);

  // Auto-scroll to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const sendMessage = async (text) => {
    if (!text.trim() || loading) return;
    if (!datasetId) {
      setMessages(prev => [
        ...prev,
        { role: 'user', content: text },
        { role: 'assistant', content: 'Please upload a dataset first so I can answer your questions about it. Click the "Upload Data" button to get started!' },
      ]);
      setInput('');
      return;
    }

    const userMessage = { role: 'user', content: text };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const response = await api.sendChat(datasetId, text);
      setMessages(prev => [
        ...prev,
        { role: 'assistant', content: response.reply },
      ]);
      if (response.suggestions && response.suggestions.length > 0) {
        setSuggestions(response.suggestions);
      }
    } catch (err) {
      setMessages(prev => [
        ...prev,
        {
          role: 'assistant',
          content: 'Sorry, I had trouble processing that. Please try again or rephrase your question.',
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage(input);
    }
  };

  return (
    <>
      {/* Chat Toggle Button */}
      <button
        className="chat-toggle"
        onClick={onToggle}
        id="chat-toggle-btn"
        title="Ask AI about your data"
      >
        {show ? '✕' : '💬'}
      </button>

      {/* Chat Panel */}
      {show && (
        <div className="chat-panel">
          {/* Header */}
          <div className="chat-header">
            <div className="chat-header-title">
              <span>🧠</span> SmartPredict AI
            </div>
            <span className="badge badge-emerald" style={{ fontSize: '0.7rem' }}>
              {hasData ? 'Data Connected' : 'No Data'}
            </span>
          </div>

          {/* Messages */}
          <div className="chat-messages">
            {messages.map((msg, i) => (
              <div
                key={i}
                className={`chat-message ${msg.role}`}
              >
                {msg.content}
              </div>
            ))}

            {/* Typing indicator */}
            {loading && (
              <div className="typing-indicator">
                <div className="typing-dot" />
                <div className="typing-dot" />
                <div className="typing-dot" />
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>

          {/* Suggestions */}
          {suggestions.length > 0 && !loading && (
            <div className="chat-suggestions">
              {suggestions.map((s, i) => (
                <button
                  key={i}
                  className="chat-suggestion"
                  onClick={() => sendMessage(s)}
                >
                  {s}
                </button>
              ))}
            </div>
          )}

          {/* Input */}
          <div className="chat-input-area">
            <input
              className="input"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Ask about your data..."
              disabled={loading}
              id="chat-input"
            />
            <button
              className="chat-send"
              onClick={() => sendMessage(input)}
              disabled={!input.trim() || loading}
              id="chat-send-btn"
            >
              ➤
            </button>
          </div>
        </div>
      )}
    </>
  );
}
