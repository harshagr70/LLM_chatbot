import { motion } from "framer-motion";

const Message = ({ text, sender }) => {
  const isUser = sender === "user";

  return (
    <motion.div
      initial={{ opacity: 0, x: isUser ? 50 : -50 }}
      animate={{ opacity: 1, x: 0 }}
      className={`p-3 rounded-lg text-white ${
        isUser ? "bg-blue-500 self-end" : "bg-gray-600 self-start"
      }`}
    >
      {text}
    </motion.div>
  );
};

export default Message;
