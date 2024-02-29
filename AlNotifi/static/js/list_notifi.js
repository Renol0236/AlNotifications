$(document).ready(function () {
    function loadNotifications() {
        var currentUrl = window.location.href;

        $.get('/api/list_notifications/', function (data) {
            $('#notifications-table-body').empty();
            data.forEach(function (notification) {
                var formattedTime = moment(notification.time).format('MMMM Do YYYY, h:mm:ss a');
                var row = '<tr>' +
                    '<td>' + notification.title + '</td>' +
                    '<td>' + notification.message + '</td>' +
                    '<td>' + formattedTime + '</td>' +
                    '<td>' + (notification.is_sent ? 'Yes' : 'No') + '</td>' +
                    '<td>' +
                    '<button style="color: #d93535;" class="delete-notification-link" data-id="' + notification.id + '">Delete</button>' +
                    '</td>' +
                    '</tr>';
                $('#notifications-table-body').append(row);
            });
        });
    }

    $(document).on('click', '.delete-notification-link', function () {
        var notificationId = $(this).data('id');
        var deleteUrl = '/api/delete_notification/' + notificationId + '/';

        $('#confirmation-modal').modal('show');

        $('#confirm-delete').on('click', function () {
            $.ajax({
                url: deleteUrl,
                type: 'DELETE',
                headers: { 'X-CSRFToken': getCookie('csrftoken') },
                success: function () {
                    location.reload();
                },
                error: function (error) {
                    console.error('Error deleting notification:', error);
                }
            });
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

    loadNotifications();
});
