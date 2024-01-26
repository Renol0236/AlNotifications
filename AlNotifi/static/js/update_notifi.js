$(document).ready(function () {
    $(document).on('submit', 'form', function(event) {
        event.preventDefault();

        var form = $(this);
        var data = form.serialize();
        var notificationId = form.find('#update_notification').data('id');

        var title = form.find('#title').val();
        var message = form.find('#message').val();
        var time = form.find('#time').val();

        data += '&title=' + title + '&message=' + message + '&time=' + time;

        $.ajax({
            url: '/api/update_notification/' + notificationId + '/',
            type: 'PUT',
            data: data,
            headers: { 'X-CSRFToken': getCookie('csrftoken') },
            success: function () {
                updateTasks();
            },
            error: function (error) {
                console.error('Ошибка при обновлении уведомления:', error);
            }
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

    function updateTasks() {
        location.reload();
    }
});
