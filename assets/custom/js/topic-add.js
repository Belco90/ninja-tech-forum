$(document).ready(function () {
  var $addTopicButton = $('#add-topic-button');
  var $addTopicTitle = $('#add-topic-title');
  var $addTopicText = $('#add-topic-text');
  var $addTopicSum = $('#add-topic-sum');

  $addTopicButton.on('click', function (event) {
    var error = false;

    if ($addTopicSum.val() !== '10') {
      error = true;
      event.preventDefault();
      $addTopicSum.closest('.form-group').addClass('has-error has-feedback');
      $addTopicSum.siblings('.form-control-feedback, .help-block').removeClass('hidden');
    } else {
      $addTopicSum.closest('.form-group').removeClass('has-error has-feedback');
      $addTopicSum.siblings('.form-control-feedback, .help-block').addClass('hidden');
    }

    if ($addTopicText.val() === '' || $addTopicTitle.val() === '') {
      error = true;
    }

    if (!error) {
      $addTopicButton.addClass('hidden');
    }

  });
});