import React from "react";
import Chatbot from "./components/Chatbot";

function App() {
  return (
    <div className="relative min-h-screen flex justify-center items-center bg-black overflow-hidden">
      <div className="absolute inset-0 bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500 blur-[150px] opacity-40 animate-pulse"></div>
      <Chatbot />
    </div>
  );
}

export default App;
