import React, { useState, useRef, useEffect } from 'react';
import Header from '../components/layout/Header';
import MessageBubble from '../components/chat/MessageBubble';
import ChatInput from '../components/chat/ChatInput';
import ThinkingIndicator from '../components/chat/ThinkingIndicator';
import { queryAssistant } from '../services/api';

const ChatPage = () => {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);

  const handleSendMessage = async (input) => {
    const userMsg = { role: "user", content: input };
    setMessages(prev => [...prev, userMsg]);
    setLoading(true);

    try {
      const response = await queryAssistant("default_session", input);
      
      const aiMsg = { 
        role: "assistant", 
        content: response.reply, 
        domain: response.domain 
      };
      
      // Speak the response
      if ('speechSynthesis' in window) {
        const utterance = new SpeechSynthesisUtterance(response.reply);
        window.speechSynthesis.speak(utterance);
      }
      
      setMessages(prev => [...prev, aiMsg]);
    } catch (error) {
      setMessages(prev => [...prev, { role: "assistant", content: "Error: Unable to connect to the intelligence core." }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-screen bg-slate-50 font-sans text-slate-800 selection:bg-indigo-100">
      <Header />
      
      <main className="flex-1 overflow-y-auto p-6 space-y-6 scroll-smooth pb-32">
        {messages.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full text-slate-400 space-y-6 max-w-lg mx-auto text-center mt-12 animate-fade-in-up">
            <div className="w-24 h-24 bg-gradient-to-tr from-indigo-100 to-blue-50 rounded-full flex items-center justify-center shadow-inner">
              <svg xmlns="http://www.w3.org/w3.org/2000/svg" className="h-10 w-10 text-indigo-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
              </svg>
            </div>
            <div>
              <h2 className="text-2xl font-bold text-slate-700 mb-2">How can I assist you?</h2>
              <p className="text-slate-500 leading-relaxed">
                I can help you navigate university documents, company HR policies, or answer general questions.
              </p>
            </div>
            
            <div className="grid grid-cols-2 gap-3 w-full mt-4">
              <button onClick={() => handleSendMessage("What are the placement statistics for Siddhartha Academy?")} className="text-left px-4 py-3 bg-white border border-slate-200 rounded-xl text-sm text-slate-600 shadow-sm hover:border-indigo-300 hover:shadow-md transition-all">
                <span className="block text-indigo-500 font-bold mb-1 text-xs uppercase tracking-wider">University Data</span>
                What are the placement statistics?
              </button>
              <button onClick={() => handleSendMessage("Tell me about Infosys HR policies.")} className="text-left px-4 py-3 bg-white border border-slate-200 rounded-xl text-sm text-slate-600 shadow-sm hover:border-indigo-300 hover:shadow-md transition-all">
                <span className="block text-blue-500 font-bold mb-1 text-xs uppercase tracking-wider">Company Data</span>
                Tell me about Infosys HR policies
              </button>
            </div>
          </div>
        ) : (
          <div className="max-w-4xl mx-auto space-y-6">
            {messages.map((m, i) => (
              <MessageBubble key={i} message={m} />
            ))}
            {loading && <ThinkingIndicator />}
            <div ref={messagesEndRef} />
          </div>
        )}
      </main>

      <div className="absolute bottom-0 left-0 right-0">
        <ChatInput onSendMessage={handleSendMessage} disabled={loading} />
      </div>
    </div>
  );
};

export default ChatPage;
