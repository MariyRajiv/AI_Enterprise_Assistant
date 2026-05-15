import React, { useState, useEffect } from 'react';

const ThinkingIndicator = () => {
  const messages = [
    "Analyzing query...",
    "Searching university documents...",
    "Checking company policies...",
    "Routing to specialized agent...",
    "Synthesizing response..."
  ];
  
  const [msgIndex, setMsgIndex] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setMsgIndex((prev) => (prev + 1) % messages.length);
    }, 1500);
    return () => clearInterval(interval);
  }, [messages.length]);

  return (
    <div className="flex justify-start animate-fade-in">
      <div className="bg-white/80 backdrop-blur border border-slate-200/50 text-slate-500 rounded-2xl rounded-bl-none p-4 shadow-sm flex items-center space-x-3">
        <div className="flex space-x-1.5">
          <div className="w-2 h-2 bg-indigo-500 rounded-full animate-bounce"></div>
          <div className="w-2 h-2 bg-indigo-500 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
          <div className="w-2 h-2 bg-indigo-500 rounded-full animate-bounce" style={{ animationDelay: '0.4s' }}></div>
        </div>
        <span className="text-sm font-medium text-indigo-500 animate-pulse">{messages[msgIndex]}</span>
      </div>
    </div>
  );
};

export default ThinkingIndicator;
