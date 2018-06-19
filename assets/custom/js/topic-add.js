function getRandomInt(min, max) {
  min = Math.ceil(min);
  max = Math.floor(max);
  return Math.floor(Math.random() * (max - min)) + min;
}

$(document).ready(function () {
  var $addTopicButton = $('#add-topic-button');
  var $addTopicTitle = $('#add-topic-title');
  var $addTopicText = $('#add-topic-text');
  var $addTopicSum = $('#add-topic-sum');
  var $topicSumLabel = $('#topic-sum-label');

  var firstRandom = getRandomInt(1, 10);
  var secondRandom = getRandomInt(1, 10);

  $topicSumLabel.text('What is the sum of ' + firstRandom + ' and ' + secondRandom + '?');

  $addTopicButton.on('click', function (event) {
    var error = false;
    var userSum = parseInt($addTopicSum.val());

    if (userSum !== (firstRandom + secondRandom)) {
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