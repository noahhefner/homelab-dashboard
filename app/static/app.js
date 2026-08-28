document.addEventListener("DOMContentLoaded", function () {
  // Bookmark group collapse/expand using Bootstrap's Collapse component,
  // with open/closed state persisted to localStorage across visits.
  var STORAGE_KEY = function (id) {
    return "homelab:group:collapsed:" + id;
  };

  function readPersisted(id) {
    try {
      return localStorage.getItem(STORAGE_KEY(id)) === "1";
    } catch (e) {
      return false;
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

    function apply(state) {
      // state === true means "collapsed"
      target.classList.toggle("show", !state);
      button.classList.toggle("collapsed", state);
      button.setAttribute("aria-expanded", String(!state));
    }

    // Initialize from persisted state on load.
    apply(readPersisted(id));

    // Persist on every show/hide triggered by Bootstrap.
    target.addEventListener("show.bs.collapse", function () {
      writePersisted(id, false);
    });
    target.addEventListener("hide.bs.collapse", function () {
      writePersisted(id, true);
    });
  });

  // Service icon fallback handled inline via onerror on each <img>.
});
