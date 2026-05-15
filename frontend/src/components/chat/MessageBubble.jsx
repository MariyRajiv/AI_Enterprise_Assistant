import React from 'react';

const MessageBubble = ({ message }) => {
  const isUser = message.role === 'user';
  
  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} animate-fade-in-up`}>
      <div className={`max-w-[80%] rounded-2xl p-4 shadow-md transition-all duration-300 ${
        isUser 
          ? 'bg-gradient-to-br from-blue-600 to-indigo-600 text-white rounded-br-none' 
          : 'bg-white/90 backdrop-blur text-slate-800 border border-slate-200/50 rounded-bl-none'
      }`}>
        <p className="whitespace-pre-wrap leading-relaxed font-medium">{message.content}</p>
        
        {message.domain && (
          <div className="mt-3 text-[10px] flex items-center gap-1.5 text-slate-400 font-bold tracking-wider">
            <svg xmlns="http://www.w3.org/w3.org/2000/svg" className="h-3.5 w-3.5 text-indigo-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            SOURCE: <span className="uppercase text-indigo-500 bg-indigo-50 px-2 py-0.5 rounded-md">{message.domain}</span>
          </div>
        )}
      </div>
    </div>
  );
};

export default MessageBubble;
