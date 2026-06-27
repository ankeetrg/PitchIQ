import type { Config } from 'tailwindcss'

const config: Config = {
  darkMode: ['selector', '[data-theme="dark"]'],
  content: ['./app/**/*.{ts,tsx}', './components/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        navy: { DEFAULT: '#091525', 2: '#0C1C2E' },
        gold: { DEFAULT: '#D97706', hover: '#B45309', dim: 'rgba(217,119,6,0.10)', border: 'rgba(217,119,6,0.24)' },
        green: { DEFAULT: '#00963F', hover: '#007B33', dim: 'rgba(0,150,63,0.10)', border: 'rgba(0,150,63,0.22)' },
        red: { DEFAULT: '#DC2626', dim: 'rgba(220,38,38,0.10)' },
        blue: { DEFAULT: '#2563EB', dim: 'rgba(37,99,235,0.10)' },
      },
      fontFamily: {
        cond: ['"Barlow Condensed"', 'Arial Narrow', 'sans-serif'],
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
}

export default config
