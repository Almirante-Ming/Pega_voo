const isDark = ref(false);
const userColors = ref<Record<string, string> | null>(null);

const convertToKebabCase = (str: string) => {
  return str.replace(/[A-Z]/g, (match) => `-${match.toLowerCase()}`);
};

const applyColors = (colors: Record<string, string>) => {
  if (import.meta.client) {
    const root = document.documentElement;
    for (const [key, value] of Object.entries(colors)) {
      if (key !== "theme") {
        const cssVar = `--${convertToKebabCase(key)}`;
        root.style.setProperty(cssVar, value);
      }
    }
  }
};

const toggleTheme = () => {
  isDark.value = !isDark.value;

  if (import.meta.client) {
    const html = document.documentElement;
    if (isDark.value) {
      html.classList.add("dark");
      localStorage.setItem("theme", "dark");
    } else {
      html.classList.remove("dark");
      localStorage.setItem("theme", "light");
    }
  }
};

const setTheme = (theme: "light" | "dark") => {
  isDark.value = theme === "dark";

  if (import.meta.client) {
    const html = document.documentElement;
    if (theme === "dark") {
      html.classList.add("dark");
      localStorage.setItem("theme", "dark");
    } else {
      html.classList.remove("dark");
      localStorage.setItem("theme", "light");
    }
  }
};

const setThemeColors = (colors: Record<string, string>) => {
  applyColors(colors);
  userColors.value = colors;

  if (colors.theme === "dark") {
    setTheme("dark");
  } else {
    setTheme("light");
  }
};

const initTheme = () => {
  if (import.meta.client) {
    const savedTheme = localStorage.getItem("theme");
    const systemPrefersDark = window.matchMedia(
      "(prefers-color-scheme: dark)"
    ).matches;

    const initialTheme = savedTheme || (systemPrefersDark ? "dark" : "light");
    setTheme(initialTheme as "light" | "dark");
  }
};

export function useTheme() {
  return {
    isDark: readonly(isDark),
    userColors: readonly(userColors),
    toggleTheme,
    setTheme,
    setThemeColors,
    initTheme,
  };
}
