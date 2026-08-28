document.addEventListener("DOMContentLoaded", function () {
  // Bookmark group collapse/expand with localStorage persistence.
  var STORAGE_KEY = function (id) {
    return "homelab:group:collapsed:" + id;
  };

  var toggles = document.querySelectorAll("[data-group-toggle]");
  toggles.forEach(function (button) {
    var groupEl = button.closest(".bookmark-group");
    var content = groupEl ? groupEl.querySelector("[data-group-content]") : null;
    if (!groupEl || !content) return;

    var id = button.getAttribute("data-group-id") || "";
    var collapsed = false;
    try {
      collapsed = localStorage.getItem(STORAGE_KEY(id)) === "1";
    } catch (e) {
      collapsed = false;
    }

    function apply(state) {
      content.classList.toggle("uk-hidden", state);
      button.classList.toggle("is-collapsed", state);
    }

    // Initialize from persisted state on load.
    apply(collapsed);

    button.addEventListener("click", function () {
      collapsed = !collapsed;
      try {
        localStorage.setItem(STORAGE_KEY(id), collapsed ? "1" : "0");
      } catch (e) {
        // storage unavailable (e.g. private mode) - state still toggles this visit
      }
      apply(collapsed);
    });
  });

  // Service icon fallback handled inline via onerror on each <img>.
});
