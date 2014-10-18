$(document).ready(function(){
  $('a.registration').click(function() {
    $('.registration-form-wrapper').fadeIn();
    $('body').addClass('popup-active');
  })
  $('a.login').click(function() {
    $('.login-form-wrapper').fadeIn();
    $('body').addClass('popup-active');
  })
  $('a.exit').click(function() {
    $(this).parent().hide();
    $('body').removeClass('popup-active');
  })
});
