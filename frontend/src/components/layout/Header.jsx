import React from 'react';

const Header = () => {
  return (
    <div className="bg-white/80 backdrop-blur-md p-4 flex justify-between items-center shadow-sm border-b border-slate-200/50 z-10 sticky top-0">
      <div className="flex items-center space-x-3">
        <div className="h-10 w-10 bg-gradient-to-br from-indigo-500 to-blue-600 rounded-xl flex items-center justify-center shadow-lg transform rotate-3">
          <svg xmlns="http://www.w3.org/w3.org/2000/svg" className="h-6 w-6 text-white transform -rotate-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.71-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
          </svg>
        </div>
        <div>
          <h1 className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-indigo-600 to-blue-600">Enterprise AI</h1>
          <p className="text-xs font-semibold text-slate-400 tracking-wide">RAG & AGENTIC WORKFLOWS</p>
        </div>
      </div>
      <div className="flex items-center space-x-2">
        <span className="flex h-2 w-2 relative">
          <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
          <span className="relative inline-flex rounded-full h-2 w-2 bg-green-500"></span>
        </span>
        <div className="bg-slate-100 px-3 py-1.5 rounded-lg text-xs font-bold text-slate-500 tracking-wide border border-slate-200">
          MISTRAL <span className="text-indigo-500 mx-1">●</span> CHROMA
        </div>
      </div>
    </div>
  );
};

export default Header;
