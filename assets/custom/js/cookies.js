$(document).ready(function () {
  var $cookiesAcceptButton = $('#cookies-accept-button');
  var $cookiesAcceptAlert = $('#cookies-accept-alert');
  var $cookiesWarningAlert = $('#cookies-warning-alert');

  $cookiesAcceptButton.on('click', function () {
    $.ajax({
      url: '/set-cookie',
      method: 'POST',
      success: function (data) {
        if (data.accepted) {
          $cookiesAcceptAlert.remove();
          $cookiesWarningAlert.remove();
        } else {
          $cookiesWarningAlert.removeClass('hidden');
        }
      },
      error: function () {
        $cookiesWarningAlert.removeClass('hidden');
      }
    });
  });
});