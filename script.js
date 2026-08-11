(function () {
  var root = document.documentElement;
  var toggle = document.getElementById("theme-toggle");
  var yearEl = document.getElementById("year");
  var STORAGE_KEY = "resume-theme";
  var SECTION_KEY = "resume-open-sections";

  if (yearEl) yearEl.textContent = String(new Date().getFullYear());

  function getInitialTheme() {
    var saved = localStorage.getItem(STORAGE_KEY);
    if (saved === "light" || saved === "dark") return saved;
    return window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  }

  function applyTheme(theme) {
    root.setAttribute("data-theme", theme);
    if (toggle) {
      var isDark = theme === "dark";
      toggle.setAttribute("aria-pressed", String(isDark));
      toggle.textContent = isDark ? "Switch to Light" : "Switch to Dark";
    }
  }

  applyTheme(getInitialTheme());

  if (toggle) {
    toggle.addEventListener("click", function () {
      var current = root.getAttribute("data-theme") || "light";
      var next = current === "dark" ? "light" : "dark";
      applyTheme(next);
      localStorage.setItem(STORAGE_KEY, next);
    });
  }

  var allDetails = Array.prototype.slice.call(document.querySelectorAll("main details"));
  var savedOpen = JSON.parse(localStorage.getItem(SECTION_KEY) || "[]");

  allDetails.forEach(function (el, idx) {
    if (!el.id) el.id = "section-" + (idx + 1);
    if (savedOpen.indexOf(el.id) !== -1) el.open = true;

    el.addEventListener("toggle", function () {
      var openIds = allDetails.filter(function (d) { return d.open; }).map(function (d) { return d.id; });
      localStorage.setItem(SECTION_KEY, JSON.stringify(openIds));
    });
  });

  if (window.location.hash) {
    var target = document.querySelector(window.location.hash);
    if (target) {
      var detailsParent = target.closest("details");
      if (detailsParent) detailsParent.open = true;
    }
  }

  // Optional analytics hook:
  // window.addEventListener("load", function () {
  //   if (typeof gtag === "function") {
  //     gtag("event", "resume_page_view", { page_title: document.title });
  //   }
  // });
})();
