$(document).ready(function () {
    $('.table').DataTable({
      responsive: true,
      dom: 'Bfrtip',
        buttons: ['copy', 'csv', 'excel', 'pdf', 'print'],
      language: {
        url: '//cdn.datatables.net/plug-ins/1.13.6/i18n/es-ES.json'
      }
    });
  });


document.addEventListener('DOMContentLoaded', function () {
  const deleteButtons = document.querySelectorAll('.btn-delete');

  deleteButtons.forEach(function (btn) {
    btn.addEventListener('click', function (e) {
      e.preventDefault(); // Previene navegación automática
      const url = btn.getAttribute('data-url');

      Swal.fire({
        title: '¿Estás seguro?',
        text: "Esta acción no se puede deshacer.",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#d33',
        cancelButtonColor: '#6c757d',
        confirmButtonText: 'Sí, borrar',
        cancelButtonText: 'Cancelar'
      }).then((result) => {
        if (result.isConfirmed) {
          window.location.href = url; // Redirecciona a la URL de eliminación
        }
      });
    });
  });
});