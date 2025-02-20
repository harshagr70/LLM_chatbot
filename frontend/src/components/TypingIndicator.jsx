import { motion } from "framer-motion";

const TypingIndicator = () => {
  return (
    <motion.div
      initial={{ opacity: 0.3 }}
      animate={{ opacity: 1 }}
      transition={{ repeat: Infinity, duration: 0.6, ease: "easeInOut" }}
      className="flex space-x-2 p-2"
    >
      <span className="w-2 h-2 bg-white rounded-full animate-bounce"></span>
      <span className="w-2 h-2 bg-white rounded-full animate-bounce delay-75"></span>
      <span className="w-2 h-2 bg-white rounded-full animate-bounce delay-150"></span>
    </motion.div>
  );
};

export default TypingIndicator;
