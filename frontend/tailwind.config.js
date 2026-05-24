/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#FB7299',
        secondary: '#00A1D6',
        bg: '#FFFFFF',
        text: '#212121',
        textLight: '#9499A0'
      }
    },
  },
  plugins: [],
}
