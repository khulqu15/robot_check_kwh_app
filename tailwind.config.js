/** @type {import('tailwindcss').Config} */
export default {
  content: [
    // this project is ionic vue typescript
    './src/**/*.{vue,js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {},
  },
  plugins: [
    require('daisyui')
  ],
}