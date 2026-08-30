document.addEventListener("DOMContentLoaded", function () {
  // Bookmark group collapse/expand using Bootstrap's Collapse component,
  // with open/closed state persisted to localStorage across visits.
  var STORAGE_KEY = function (id) {
    return "homelab:group:collapsed:" + id;
  };

  function readPersistedOrNull(id) {
    try {
      var value = localStorage.getItem(STORAGE_KEY(id));
      if (value === null) return null;
      return value === "1";
    } catch (e) {
      return null;
    }
  }

  function writePersisted(id, collapsed) {
    try {
      localStorage.setItem(STORAGE_KEY(id), collapsed ? "1" : "0");
    } catch (e) {
      // storage unavailable (e.g. private mode) - state still toggles this visit
    }
  }

  var toggles = document.querySelectorAll("[data-group-toggle]");

  toggles.forEach(function (button) {
    var target = document.querySelector(button.getAttribute("data-bs-target"));
    if (!target) return;

    var collapse = window.bootstrap.Collapse.getOrCreateInstance(target, {
      toggle: false,
    });

    var id = button.getAttribute("data-group-id") || "";

    // Config-derived default state: the per-group `collapsed` option rendered
    // as `data-default-collapsed="true|false"`. Defaults to open when absent to
    // preserve existing behavior.
    var defaultCollapsed = button.getAttribute("data-default-collapsed") === "true";

    function apply(state) {
      // state === true means "collapsed"
      target.classList.toggle("show", !state);
      button.classList.toggle("collapsed", state);
      button.setAttribute("aria-expanded", String(!state));
    }

    // Initialize from a persisted user choice when present; otherwise fall back
    // to the config default. A saved choice always takes precedence.
    var saved = readPersistedOrNull(id);
    apply(saved !== null ? saved : defaultCollapsed);

    // Persist on every show/hide triggered by Bootstrap.
    target.addEventListener("show.bs.collapse", function () {
      writePersisted(id, false);
    });
    target.addEventListener("hide.bs.collapse", function () {
      writePersisted(id, true);
    });
  });

  // Service icon fallback handled inline via onerror on each <img>.

  // ---- Dark mode toggle ----
  // Theme preference persisted to localStorage across visits, mirroring the
  // bookmark-collapse pattern above. Defaults to the system preference, else
  // light.
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
