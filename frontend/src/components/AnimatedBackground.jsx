import { motion } from "framer-motion";

const AnimatedBackground = () => {
  return (
    <div className="absolute inset-0 bg-black overflow-hidden">
      {/*  Moving Gradient Background */}
      <motion.div
        className="absolute inset-0 bg-gradient-to-br from-indigo-500 to-purple-700"
        animate={{ scale: [3, 1.1, 3] }}
        transition={{ duration: 10, repeat: Infinity, ease: "easeInOut" }}
      ></motion.div>

      {/*  Glowing Effect (Full Page) */}
      <div className="absolute inset-0 bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500 blur-[150px] opacity-40 animate-pulse"></div>
    </div>
  );
};

export default AnimatedBackground;
