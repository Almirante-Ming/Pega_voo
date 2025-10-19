module.exports = {
  content: [
    "./Components/**/*.{js,vue,ts}",
    "./components/**/*.{js,vue,ts}",
    "./layouts/**/*.vue",
    "./pages/**/*.vue",
    "./plugins/**/*.{js,ts}",
    "./app.vue",
    "./error.vue",
  ],
  theme: {
    extend: {
      colors: {
        primary: "var(--primary)",
        "primary-light": "var(--primary-light)",
        "primary-dark": "var(--primary-dark)",

        secondary: "var(--secondary)",
        "secondary-light": "var(--secondary-light)",
        "secondary-dark": "var(--secondary-dark)",

        "grayScale-50": "var(--grayScale-50)",
        "grayScale-100": "var(--grayScale-100)",
        "grayScale-200": "var(--grayScale-200)",
        "grayScale-300": "var(--grayScale-300)",
        "grayScale-400": "var(--grayScale-400)",
        "grayScale-500": "var(--grayScale-500)",
        "grayScale-600": "var(--grayScale-600)",
        "grayScale-700": "var(--grayScale-700)",
        "grayScale-800": "var(--grayScale-800)",
        "grayScale-900": "var(--grayScale-900)",
        "grayScale-950": "var(--grayScale-950)",

        "input-100": "var(--input-100)",
        "input-200": "var(--input-200)",

        "text-color": "var(--text-color)",
        "text-secondary": "var(--text-secondary)",
        black: "var(--black)",
        white: "var(--white)",
        background: "var(--background)",

        error: "var(--error)",
        warning: "var(--warning)",
        success: "var(--success)",
      },
      fontFamily: {
        inter: ["Inter", "sans-serif"],
        montserrat: ["Montserrat", "sans-serif"],
        nunito: ["Nunito", "sans-serif"],
        roboto: ["Roboto", "sans-serif"],
      },
    },
  },
  darkMode: "class",
};
