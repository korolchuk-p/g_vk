$(document).keyup(function(e) {
  if (e.keyCode == 27) {
    $('a.exit').click();
  }
});
$(document).ready(function() {
  $('a.registration').click(function() {
    $('.registration-form-wrapper').fadeIn();
    $('.popup-background').fadeIn();
  });
  $('a.login').click(function() {
    $('.login-form-wrapper').fadeIn();
    $('.popup-background').fadeIn();
  });
  $('a.exit').click(function() {
    $(this).parent().hide();
    $('.popup-background').hide();
  });
  $('.popup-background').click(function() {
    $('.form-wrapper:visible').hide();
    $(this).hide();
  });
  $('.form-wrapper input[type="submit"]').one().click(function() {
    var elemName = $(this).siblings('input[name="user"]');
    var elemPass = $(this).siblings('input[name="pass"]');
    var elemRe_pass = $(this).siblings('input[name="re_pass"]');
    var name = $(elemName).val();
    var pass = $(elemPass).val();
    var re_pass = $(elemRe_pass).val();
    if (name.length < 1) {
      $('.error-message').remove();
      $(elemName).before('<div class="error-message">field is required</div>');
      return false;
    }
    if (name.length > 32) {
      $('.error-message').remove();
      $(elemName).before('<div class="error-message">name is too long</div>');
      return false;
    }
    if (pass.length < 1) {
      $('.error-message').remove();
      $(elemPass).before('<div class="error-message">field is required</div>');
      return false;
    }
    if (pass.length > 32) {
      $('.error-message').remove();
      $(elemPass).before('<div class="error-message">password is too long</div>');
      return false;
    }
    if (pass != re_pass) {
      $('.error-message').remove();
      $(elemPass).before('<div class="error-message">passwords do not mutch</div>');
      return false;
    }
  });
});
