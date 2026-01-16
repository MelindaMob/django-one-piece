/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'op-red': '#DC143C',
        'op-blue': '#1E90FF',
        'op-yellow': '#FFD700',
        'op-orange': '#FF8C00',
        'op-dark': '#1a1a2e',
        'op-navy': '#16213e',
        'op-gold': '#D4AF37',
      },
      fontFamily: {
        'sans': ['Inter', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
}

