import React, { useState, useEffect, useRef } from 'react';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import './styles.css';

interface SourceReference {
  chapter_title: string;
  section_title: string;
  module: string;
  url: string;
  relevance_score: number;
}

interface QueryResponse {
  answer: string;
  sources: SourceReference[];
  confidence: string;
  mode_used: string;
  chunks_retrieved: number;
}

interface Message {
  role: 'user' | 'assistant';
  content: string;
  sources?: SourceReference[];
  confidence?: string;
}

const STORAGE_KEYS = {
  MESSAGES: 'chatbot_messages',
  IS_OPEN: 'chatbot_is_open',
  PERSONA: 'chatbot_persona',
};

export default function ChatWidget() {
  // Get API_URL from Docusaurus custom fields
  const { siteConfig } = useDocusaurusContext();
  const API_URL = (siteConfig.customFields?.API_URL as string) || 'http://localhost:8001';

  const [isOpen, setIsOpen] = useState(() => {
    if (typeof window !== 'undefined') {
      const stored = sessionStorage.getItem(STORAGE_KEYS.IS_OPEN);
      return stored === 'true';
    }
    return false;
  });

  const [messages, setMessages] = useState<Message[]>(() => {
    if (typeof window !== 'undefined') {
      const stored = sessionStorage.getItem(STORAGE_KEYS.MESSAGES);
      return stored ? JSON.parse(stored) : [];
    }
    return [];
  });

  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [mode, setMode] = useState<'global' | 'selected'>('global');
  const [selectedText, setSelectedText] = useState('');

  const [persona, setPersona] = useState<string>(() => {
    if (typeof window !== 'undefined') {
      return sessionStorage.getItem(STORAGE_KEYS.PERSONA) || '';
    }
    return '';
  });

  const messagesEndRef = useRef<HTMLDivElement>(null);
  const abortControllerRef = useRef<AbortController | null>(null);

  // Save messages to sessionStorage whenever they change
  useEffect(() => {
    if (typeof window !== 'undefined' && messages.length > 0) {
      sessionStorage.setItem(STORAGE_KEYS.MESSAGES, JSON.stringify(messages));
    }
  }, [messages]);

  // Save isOpen state to sessionStorage
  useEffect(() => {
    if (typeof window !== 'undefined') {
      sessionStorage.setItem(STORAGE_KEYS.IS_OPEN, String(isOpen));
    }
  }, [isOpen]);

  // Save persona to sessionStorage
  useEffect(() => {
    if (typeof window !== 'undefined') {
      sessionStorage.setItem(STORAGE_KEYS.PERSONA, persona);
    }
  }, [persona]);

  // Scroll to bottom when messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Listen for text selection on the page
  useEffect(() => {
    const handleSelectionChange = () => {
      const selection = window.getSelection();
      const text = selection?.toString().trim();
      if (text && text.length >= 10) {
        setSelectedText(text);
        setMode('selected');
      }
    };

    document.addEventListener('mouseup', handleSelectionChange);
    return () => document.removeEventListener('mouseup', handleSelectionChange);
  }, []);

  // Cleanup: Cancel in-flight requests on component unmount
  useEffect(() => {
    return () => {
      if (abortControllerRef.current) {
        abortControllerRef.current.abort();
      }
    };
  }, []);

  const queryWithRetry = async (userMessage: string, retryCount = 0): Promise<QueryResponse> => {
    const maxRetries = 1;
    const timeout = 60000; // 60 seconds (RAG queries can be slow)

    // Create AbortController for timeout and store in ref
    const abortController = new AbortController();
    abortControllerRef.current = abortController;
    const timeoutId = setTimeout(() => abortController.abort(), timeout);

    try {
      const response = await fetch(`${API_URL}/query`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          question: userMessage,
          mode: mode,
          selected_text: mode === 'selected' ? selectedText : undefined,
          persona: persona || undefined,
        }),
        signal: abortController.signal,
      });

      clearTimeout(timeoutId);

      if (!response.ok) {
        if (response.status === 400) {
          try {
            const errorData = await response.json();
            throw new Error(`Bad request: ${errorData.detail || 'Invalid query format'}`);
          } catch (parseError) {
            throw new Error('Bad request: Invalid query format');
          }
        } else if (response.status === 500) {
          throw new Error('Server error: The server encountered an error. Please try again.');
        } else {
          throw new Error(`HTTP ${response.status}: Request failed`);
        }
      }

      // Parse JSON response with error handling
      let data: QueryResponse;
      try {
        data = await response.json();
      } catch (parseError) {
        throw new Error('Parse error: Received malformed response from server. Please try again.');
      }

      return data;
    } catch (error) {
      clearTimeout(timeoutId);

      // Handle timeout (AbortError)
      if (error.name === 'AbortError') {
        throw new Error('Timeout: The server is taking too long to respond. Please try again.');
      }

      // Handle network failures
      if (error.message.includes('Failed to fetch') || error.message.includes('NetworkError')) {
        throw new Error('Connection failed: Unable to connect to the chatbot server. Please check your internet connection.');
      }

      // Retry once on failure (except for 400 errors and parse errors)
      if (retryCount < maxRetries && !error.message.includes('Bad request') && !error.message.includes('Parse error')) {
        // Wait 500ms before retry
        await new Promise(resolve => setTimeout(resolve, 500));
        return queryWithRetry(userMessage, retryCount + 1);
      }

      throw error;
    } finally {
      abortControllerRef.current = null;
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    // Prevent empty queries
    if (!input.trim()) return;

    const userMessage = input.trim();

    // Prevent queries longer than 1000 characters
    if (userMessage.length > 1000) {
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: 'Your question is too long (maximum 1000 characters). Please shorten it and try again.',
      }]);
      return;
    }

    // Handle rapid-fire queries: if already loading, queue will be processed sequentially
    if (isLoading) {
      // Simply return - user must wait for current query to complete
      return;
    }

    setInput('');
    setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
    setIsLoading(true);

    try {
      const data = await queryWithRetry(userMessage);
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: data.answer,
        sources: data.sources,
        confidence: data.confidence,
      }]);
    } catch (error) {
      // Display categorized error message
      const errorMessage = error instanceof Error ? error.message : 'An unexpected error occurred. Please try again.';
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: errorMessage,
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  const clearSelection = () => {
    setSelectedText('');
    setMode('global');
  };

  const clearHistory = () => {
    setMessages([]);
    if (typeof window !== 'undefined') {
      sessionStorage.removeItem(STORAGE_KEYS.MESSAGES);
    }
  };

  return (
    <div className="chat-widget">
      {/* Floating Button with Label */}
      {!isOpen ? (
        <div className="chat-toggle-container" onClick={() => setIsOpen(true)}>
          <div className="ai-assistant-label">
            AI Assistant
          </div>
          <div className="chat-toggle-icon">
            <span className="robot-emoji">🤖</span>
          </div>
        </div>
      ) : (
        <button
          className="chat-toggle open"
          onClick={() => setIsOpen(false)}
          aria-label="Close chat"
        >
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <line x1="18" y1="6" x2="6" y2="18"></line>
            <line x1="6" y1="6" x2="18" y2="18"></line>
          </svg>
        </button>
      )}

      {/* Chat Panel */}
      {isOpen && (
        <div className="chat-panel">
          <div className="chat-header">
            <div className="chat-header-content">
              <div className="chat-header-icon">🤖</div>
              <div className="chat-header-text">
                <h3>Ask the Textbook</h3>
                <p className="chat-header-subtitle">Powered by AI</p>
              </div>
            </div>
            <div className="chat-controls">
              <select
                value={persona}
                onChange={(e) => setPersona(e.target.value)}
                className="persona-select"
              >
                <option value="">All audiences</option>
                <option value="beginner">Beginner</option>
                <option value="software_engineer">Software Engineer</option>
                <option value="robotics_student">Robotics Student</option>
                <option value="ai_researcher">AI Researcher</option>
              </select>
              {messages.length > 0 && (
                <button
                  onClick={clearHistory}
                  className="clear-history-button"
                  title="Clear conversation history"
                >
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <polyline points="3 6 5 6 21 6"></polyline>
                    <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                  </svg>
                </button>
              )}
            </div>
          </div>

          {/* Mode indicator */}
          {mode === 'selected' && selectedText && (
            <div className="mode-indicator">
              <span>Asking about selected text</span>
              <button onClick={clearSelection} className="clear-selection">
                Clear
              </button>
            </div>
          )}

          {/* Messages */}
          <div className="chat-messages">
            {messages.length === 0 && (
              <div className="welcome-message">
                <div className="welcome-icon">🤖</div>
                <h4>Welcome to the Physical AI Textbook!</h4>
                <p className="welcome-text">Hi! I can answer questions about Physical AI & Humanoid Robotics.</p>
                <p className="welcome-quote">"Curiosity is my compass, and this book is my map."</p>
                <p className="hint">Try asking about ROS 2, digital twins, NVIDIA Isaac, or VLA models.</p>
                <div className="author-info">
                  <p className="author-name">Muhammad Zarwali</p>
                  <div className="social-links">
                    <a href="https://github.com/MuhammadZarwali" target="_blank" rel="noopener noreferrer" className="social-link" title="GitHub">
                      <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
                      </svg>
                    </a>
                    <a href="https://www.linkedin.com/in/muhammad-zarwali-b3260a2b4" target="_blank" rel="noopener noreferrer" className="social-link" title="LinkedIn">
                      <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"/>
                      </svg>
                    </a>
                  </div>
                </div>
              </div>
            )}
            {messages.map((msg, idx) => (
              <div key={idx} className={`message ${msg.role}`}>
                <div className="message-content">{msg.content}</div>
                {msg.sources && msg.sources.length > 0 && (
                  <div className="message-sources">
                    <strong>Sources:</strong>
                    <ul>
                      {msg.sources.map((src, i) => (
                        <li key={i}>
                          <a href={src.url}>{src.section_title}</a>
                          <span className="source-score">({Math.round(src.relevance_score * 100)}%)</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
                {msg.confidence && msg.confidence !== 'high' && (
                  <div className={`confidence-badge ${msg.confidence}`}>
                    {msg.confidence === 'none' ? 'Not found' :
                     msg.confidence === 'low' ? 'Low confidence' :
                     'Medium confidence'}
                  </div>
                )}
              </div>
            ))}
            {isLoading && (
              <div className="message assistant loading">
                <div className="typing-indicator">
                  <span></span><span></span><span></span>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Input */}
          <form onSubmit={handleSubmit} className="chat-input-form">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask a question..."
              disabled={isLoading}
              className="chat-input"
            />
            <button type="submit" disabled={isLoading || !input.trim()} className="send-button">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <line x1="22" y1="2" x2="11" y2="13"></line>
                <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
              </svg>
            </button>
          </form>
        </div>
      )}
    </div>
  );
}
