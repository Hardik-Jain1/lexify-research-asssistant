// tailwind.config.js
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}", // Include all relevant file types in src
  ],
  theme: {
    extend: {
      // You can extend the default theme here (e.g., custom fonts, colors)
      fontFamily: {
        sans: ['Inter', 'sans-serif'], // Example: Using Inter font
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'), // Optional: For better default form styling
    // require('daisyui'), // Optional: If you want to use DaisyUI components
  ],
  // Optional: DaisyUI config if you use it
  // daisyui: {
  //   themes: ["light", "dark", "cupcake"], // example themes
  // },
}