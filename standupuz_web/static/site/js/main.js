document.addEventListener('DOMContentLoaded', function () {
  var sidenav = document.querySelectorAll('.sidenav');
  var instances_sidenav = M.Sidenav.init(sidenav, { edge: 'right' });
  var modal = document.querySelectorAll('.modal');
  var instances_modal = M.Modal.init(modal);
});

