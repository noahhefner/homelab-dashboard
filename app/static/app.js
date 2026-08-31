document.addEventListener("DOMContentLoaded", function () {
  
  // ---- Dark mode toggle ----
  // Theme preference persisted to localStorage across visits. Defaults 
  // to the system preference, else light.
  var THEME_STORAGE_KEY = "homelab:theme";

  function readPersistedTheme() {
    try {
      return localStorage.getItem(THEME_STORAGE_KEY);
    } catch (e) {
      return null;
    }
  }

  function writePersistedTheme(theme) {
    try {
      localStorage.setItem(THEME_STORAGE_KEY, theme);
    } catch (e) {
      // storage unavailable (e.g. private mode) - theme still applies this visit
    }
  }

  function systemTheme() {
    if (window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches) {
      return "dark";
    }
    return "light";
  }

  function applyTheme(theme) {
    document.documentElement.setAttribute("data-bs-theme", theme);
    var icon = document.querySelector(".theme-toggle .theme-icon");
    if (icon) {
      // Show the moon icon in light mode (toggle acts as the switch to dark),
      // the sun icon in dark mode.
      icon.className = "bi theme-icon " + (theme === "dark" ? "bi-sun" : "bi-moon-stars");
    }
  }

  var themeToggle = document.querySelector("[data-theme-toggle]");
  if (themeToggle) {
    var initialTheme = readPersistedTheme() || systemTheme();
    applyTheme(initialTheme);

    themeToggle.addEventListener("click", function () {
      var next = document.documentElement.getAttribute("data-bs-theme") === "dark" ? "light" : "dark";
      applyTheme(next);
      writePersistedTheme(next);
    });
  }
});
