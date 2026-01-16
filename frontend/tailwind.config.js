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
        'op-red-dark': '#B71C1C',
        'op-white': '#FFFFFF',
        'op-gray': '#F5F5F5',
        'op-dark': '#1a1a1a',
      },
      fontFamily: {
        'sans': ['Noto Sans JP', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
