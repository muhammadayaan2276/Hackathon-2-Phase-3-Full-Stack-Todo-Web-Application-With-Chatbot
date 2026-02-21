'use client';

import { useState, useEffect, useRef } from 'react';
import { isAuthenticated } from '@/lib/auth';
import { chatApi } from '@/lib/chatApi';

interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

export default function ChatBot() {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isClient, setIsClient] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Mark as client-side after mount
  useEffect(() => {
    setIsClient(true);
  }, []);

  // Scroll to bottom when messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Only show chatbot when on client side, authenticated, and not on auth pages
  if (!isClient) return null;

  const shouldShowChatbot = isAuthenticated() &&
    !window.location.pathname.startsWith('/login') &&
    !window.location.pathname.startsWith('/signup');

  if (!shouldShowChatbot) return null;

  const handleSendMessage = async () => {
    if (!inputValue.trim() || isLoading) return;

    // Add user message
    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      role: 'user',
      content: inputValue,
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      // Send to backend /chat endpoint
      const response = await chatApi.sendMessage(inputValue);

      // Add assistant response
      const assistantMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: response.message,
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      const errorMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const toggleChat = () => {
    setIsOpen(!isOpen);
    if (!isOpen) {
      // When opening, add a welcome message
      const welcomeMessage: ChatMessage = {
        id: 'welcome-' + Date.now(),
        role: 'assistant',
        content: 'Hello! I\'m your Todo Assistant. How can I help you manage your tasks today? I am here to provide information about your todos.',
        timestamp: new Date(),
      };
      setMessages([welcomeMessage]);
    }
  };

  const clearChat = () => {
    setMessages([]);
    setInputValue('');
  };

  return (
    <>
      {/* Floating Chat Button */}
      <button
        onClick={toggleChat}
       className="fixed bottom-6 right-6 w-14 h-14 bg-black hover:bg-gray-400 text-white rounded-full shadow-[0_0_20px_rgba(0,0,0,0.5)] flex items-center justify-center z-50 transition-all duration-300 transform hover:scale-110 "

        aria-label={isOpen ? "Close chat" : "Open chat"}
      >
        <span className="text-xl ">🤖</span>
      </button>
{isOpen && (
  <>
    {/* Proper Overlay */}
    <div
      className="fixed inset-0 bg-black/40"
      onClick={toggleChat}
    />

    {/* Floating Chat Modal */}
    <div className="fixed right-6 bottom-4 w-96 max-w-[90vw] h-[520px] bg-white rounded-2xl shadow-[0_25px_60px_rgba(0,0,0,0.35)] z-50 flex flex-col overflow-hidden">

      {/* Header */}
      <div className="bg-gradient-to-r from-blue-600 to-indigo-700 px-4 py-3 sm:py-4 flex items-center justify-between min-h-[56px] rounded-t-2xl">
        <div className="flex items-center space-x-3 flex-1">
          <div className="w-10 h-10 bg-white rounded-full flex items-center justify-center">
            🤖
          </div>
          <div className="flex-1 min-w-0">
            <h3 className="text-white font-semibold truncate">Todo Assistant</h3>
            <p className="text-blue-100 text-sm truncate">AI-powered task management</p>
          </div>
        </div>

        <button
          onClick={toggleChat}
          className="text-white hover:text-blue-200 transition-colors"
          aria-label="Close chat"
        >
          ✕
        </button>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-gray-50">
        {messages.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full text-gray-500 text-center">
            <p>
              Hi! I am your Todo Assistant.  
              I am here to provide information about your todos.
            </p>
          </div>
        ) : (
          messages.map((message) => (
            <div
              key={message.id}
              className={`flex ${
                message.role === "user"
                  ? "justify-end"
                  : "justify-start"
              }`}
            >
              <div
                className={`max-w-[80%] rounded-2xl px-4 py-3 ${
                  message.role === "user"
                    ? "bg-blue-600 text-white rounded-br-none"
                    : "bg-white border border-gray-200 rounded-bl-none shadow-sm"
                }`}
              >
                <p className="text-sm">{message.content}</p>
                <p className="text-xs mt-1 text-gray-400">
                  {message.timestamp.toLocaleTimeString([], {
                    hour: "2-digit",
                    minute: "2-digit",
                  })}
                </p>
              </div>
            </div>
          ))
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="border-t border-gray-200 p-4 bg-yellow-200">
        <div className="flex space-x-2">
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Ask about your todos..."
            className="flex-1 border border-gray-300 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
            disabled={isLoading}
          />
          <button
            onClick={handleSendMessage}
            disabled={!inputValue.trim() || isLoading}
            className="bg-indigo-900 hover:bg-gray-500 text-white px-4 py-3 rounded-lg disabled:opacity-50 transition-colors"
          >
            ➤
          </button>
        </div>
      </div>
    </div>
  </>
)}
    </>
  );
}