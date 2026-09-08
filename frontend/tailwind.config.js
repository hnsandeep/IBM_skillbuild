/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        risk: {
          low:      "#22c55e",
          medium:   "#eab308",
          high:     "#f97316",
          critical: "#ef4444",
        },
      },
      // Ensure custom animation utilities are available
      animation: {
        "fade-in":  "fadeIn 0.35s ease-out both",
        "grow-x":   "growX 0.7s cubic-bezier(0.22,1,0.36,1) both",
      },
      keyframes: {
        fadeIn: {
          from: { opacity: "0", transform: "translateY(10px)" },
          to:   { opacity: "1", transform: "translateY(0)"    },
        },
        growX: {
          from: { transform: "scaleX(0)" },
          to:   { transform: "scaleX(1)" },
        },
      },
    },
  },
  plugins: [],
};
