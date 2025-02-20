import React, { useState, useEffect, useRef } from "react";
import { FiSend } from "react-icons/fi";
import { motion } from "framer-motion"; // Importing Framer Motion for animations

const Chatbot = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const chatEndRef = useRef(null);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const newMessage = { text: input, sender: "user" };
    setMessages([...messages, newMessage]);
    setInput("");
    setLoading(true);

    try {
      const response = await fetch("http://localhost:8000/query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: input }),
      });

      const data = await response.json();
      let answer = data.final_answer || "No response";

      
      const matches = answer.match(/<Name>(.*?)<\/Name>/g);
      if (matches) {
        answer = matches.map((match) => match.replace(/<\/?Name>/g, "")).join(", ");
      }

      setMessages((prev) => [...prev, { text: answer, sender: "bot" }]);
    } catch (error) {
      setMessages((prev) => [...prev, { text: "Error fetching response!", sender: "bot" }]);
    }

    setLoading(false);
  };

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  return (
    <div className="relative flex justify-center items-center min-h-screen bg-black">
      
      <div className="absolute inset-0">
        
        <div className="absolute inset-0 bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500 blur-[180px] opacity-50 animate-pulse"></div>
        
        <div className="absolute inset-0 bg-gradient-to-r from-indigo-400 via-blue-600 to-purple-700 blur-[250px] opacity-30"></div>
      </div>

      
      <motion.h1 
        className="absolute top-5 text-white text-3xl font-bold tracking-wider"
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        Chatbot
      </motion.h1>

      
      <div className="relative w-[80vw] md:w-[60vw] lg:w-[50vw] h-[80vh] bg-gray-900 text-white rounded-lg shadow-xl overflow-hidden p-5 backdrop-blur-md border border-gray-700">
        
        
        <div className="h-[85%] overflow-y-auto space-y-3 p-2">
          {messages.map((msg, index) => (
            <motion.div 
              key={index} 
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.3 }}
              className={`p-3 rounded-lg w-fit max-w-[80%] ${msg.sender === "user" ? "bg-blue-500 ml-auto" : "bg-gray-700"}`}
            >
              {msg.text}
            </motion.div>
          ))}
          
          
          {loading && (
            <motion.div 
              className="flex space-x-1"
              animate={{ opacity: [0.3, 1, 0.3] }}
              transition={{ repeat: Infinity, duration: 1 }}
            >
              <div className="w-2 h-2 bg-gray-400 rounded-full"></div>
              <div className="w-2 h-2 bg-gray-400 rounded-full"></div>
              <div className="w-2 h-2 bg-gray-400 rounded-full"></div>
            </motion.div>
          )}

          <div ref={chatEndRef} />
        </div>

       
        <div className="absolute bottom-3 left-3 right-3 flex items-center space-x-2">
          <input
            type="text"
            className="flex-1 p-3 rounded-full bg-gray-800 text-white border border-gray-600 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500 transition-all"
            placeholder="Ask me something..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && sendMessage()}
          />

          
          <motion.button
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.9 }}
            onClick={sendMessage}
            className="p-3 rounded-lg bg-blue-600 hover:bg-blue-700 transition flex items-center justify-center"
          >
            <FiSend size={24} />
          </motion.button>
        </div>
      </div>
    </div>
  );
};

export default Chatbot;
