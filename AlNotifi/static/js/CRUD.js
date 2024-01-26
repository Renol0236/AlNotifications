$(document).ready(function() {

        $('.delete-btn').click(function() {
            var notificationId = $(this).data('notification-id');
            if (confirm("Are you sure you want to delete this notification?")) {
                $.ajax({
                    url: "/api/CRUD_notification/" + notificationId + '/',
                    type: "DELETE",
                    headers: { 'X-CSRFToken': getCookie('csrftoken') },
                    success: function(response) {
                        alert("Notification deleted successfully!");
                        location.reload();
                    },
                    error: function(xhr, errmsg, err) {
                        console.log(xhr.status + ": " + xhr.responseText);
                        alert("Failed to delete notification. Please try again later.");
                    }
                });
            }
        });

        $('.update-btn').click(function() {
            var notificationId = $(this).data('notification-id');
            alert("Update button clicked for notification with ID: " + notificationId);
        });
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