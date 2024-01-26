$(document).ready(function () {
    $(document).on('click', '.delete-notification-link', function (e) {
      e.preventDefault();

      var notificationId = $(this).data('id');

      $('#confirmation-modal').find('.modal-body p').text('Do you sure, that you want delete this notification with ID ' + notificationId + '?');

      $('#confirm-delete').data('notification-id', notificationId);

      $('#confirmation-modal').modal('show');
    });
  
    $('#confirm-delete').on('click', function () {

      var notificationId = $(this).data('notification-id');

      $.ajax({
        url: '/api/delete_notification/' + notificationId + '/',
        type: 'DELETE',
        headers: { 'X-CSRFToken': getCookie('csrftoken') },
        success: function () {

          $('#confirmation-modal').modal('hide');

          updateTasks();

        },
        error: function (error) {
          console.error('Ошибка при удалении уведомления:', error);
        }
      });
      function getCookie(name) {
      var cookieValue = null;
      if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
          var cookie = cookies[i].trim();
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
          }
        }
      }
      return cookieValue;
  }

      function updateTasks() {
          location.reload();
      }
    });
  });