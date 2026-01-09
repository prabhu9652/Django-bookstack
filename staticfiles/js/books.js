document.addEventListener('DOMContentLoaded', function () {
  var sidebar = document.getElementById('books-sidebar');
  var mobileSidebar = document.getElementById('books-sidebar-mobile');
  var toggle = document.getElementById('category-toggle');
  var collapse = document.getElementById('sidebar-collapse');
  var overlay = document.getElementById('sidebar-overlay');

  var closeMobile = document.getElementById('sidebar-close-mobile');
  if (toggle && mobileSidebar && overlay) {
    toggle.addEventListener('click', function (e) {
      e.preventDefault();
      var open = mobileSidebar.classList.toggle('open');
      overlay.classList.toggle('open', open);
      toggle.setAttribute('aria-expanded', open);
      mobileSidebar.setAttribute('aria-hidden', !open);
    });

    overlay.addEventListener('click', function () {
      mobileSidebar.classList.remove('open');
      overlay.classList.remove('open');
      toggle.setAttribute('aria-expanded', false);
      mobileSidebar.setAttribute('aria-hidden', true);
    });

    if (closeMobile) {
      closeMobile.addEventListener('click', function () {
        mobileSidebar.classList.remove('open');
        overlay.classList.remove('open');
        toggle.setAttribute('aria-expanded', false);
        mobileSidebar.setAttribute('aria-hidden', true);
      });
    }

    // close on Escape
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') {
        mobileSidebar.classList.remove('open');
        overlay.classList.remove('open');
        toggle.setAttribute('aria-expanded', false);
        mobileSidebar.setAttribute('aria-hidden', true);
      }
    });
  }

  if (collapse && sidebar) {
    collapse.addEventListener('click', function () {
      sidebar.classList.toggle('collapsed');
      collapse.setAttribute('aria-pressed', sidebar.classList.contains('collapsed'));
    });
  }

});