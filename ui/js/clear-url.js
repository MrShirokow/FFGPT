// Remove empty query parameters from URL
$(function() {
  $('form').submit(function () {
    var $empty_fields = $(this).find(':input').filter(function () {
      return $(this).val() === '';
    });
    $empty_fields.prop('disabled', true);
    return true;
  });
});
