import { useState } from 'react';
import axios from 'axios';
import './Chatbot.css';

interface SearchResult {
  rank: number;
  filename: string;
  page_number: number;
  relevance_score: number;
  preview: string;
}

interface Message {
  id: number;
  text: string;
  isUser: boolean;
  results?: SearchResult[];
}

function Chatbot() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 0,
      text: "👋 Hello! I can help you search through opioid pharmaceutical documents. Ask me questions like:\n\n• \"3: narratives about opioids as a right\"\n• \"Show me pages about pharmaceutical marketing\"\n• \"10: Walgreens opioid strategy\"\n\nTip: Start with a number and colon (e.g., \"5: your question\") to specify how many results you want!",
      isUser: false
    }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage: Message = {
      id: messages.length,
      text: input,
      isUser: true
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    // Parse the input for number of results
    let nResults = 5;
    let actualQuestion = input;

    if (input.includes(':')) {
      const parts = input.split(':', 2);
      const num = parseInt(parts[0].trim());
      if (!isNaN(num)) {
        nResults = Math.min(Math.max(num, 1), 20);
        actualQuestion = parts[1].trim();
      }
    }

    try {
      const response = await axios.post('http://localhost:5000/search', {
        question: actualQuestion,
        n_results: nResults
      });

      const botMessage: Message = {
        id: messages.length + 1,
        text: `Found ${response.data.results.length} most relevant pages:`,
        isUser: false,
        results: response.data.results
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      const errorMessage: Message = {
        id: messages.length + 1,
        text: `❌ Error: ${error instanceof Error ? error.message : 'Failed to connect to server'}`,
        isUser: false
      };
      setMessages(prev => [...prev, errorMessage]);
    }

    setLoading(false);
  };

  return (
    <div className="chatbot-container">
      <div className="chatbot-header">
        <h1>🔍 Opioid Document Search</h1>
        <p>Search across 8,822 pages from 490 PDF files</p>
      </div>

      <div className="chatbot-messages">
        {messages.map(message => (
          <div key={message.id} className={`message ${message.isUser ? 'user' : 'bot'}`}>
            <div className="message-bubble">
              {message.text}
              {message.results && (
                <div className="results-container">
                  {message.results.map(result => (
                    <div key={result.rank} className="result-card">
                      <div className="result-header">📄 Result {result.rank}</div>
                      <div className="result-meta">
                        File: {result.filename} | Page: {result.page_number}
                      </div>
                      <div className="result-preview">
                        {result.preview}...
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        ))}
        {loading && (
          <div className="message bot">
            <div className="message-bubble loading-message">
              🔍 Searching...
            </div>
          </div>
        )}
      </div>

      <div className="chatbot-input-container">
        <input
          type="text"
          className="chatbot-input"
          placeholder="Type your question here..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && handleSend()}
          disabled={loading}
        />
        <button 
          className="send-button" 
          onClick={handleSend}
          disabled={loading}
        >
          Send
        </button>
        <div className="help-text">
          Format: "number: question" (e.g., "5: opioid marketing") or just ask naturally
        </div>
      </div>
    </div>
  );
}

export default Chatbot;