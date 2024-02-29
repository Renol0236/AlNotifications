$(document).ready(function() {
  $('#confirmUnlink').click(function() {
    $.ajax({
      type: 'POST',
      url: '/ouath2/discord/unlink/',
      headers: { 'X-CSRFToken': getCookie('csrftoken') },
      data: {},
      success: function(response) {
        console.log(response);
        location.reload();
      },
      error: function(xhr, status, error) {
        console.error(xhr.responseText);
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
});


