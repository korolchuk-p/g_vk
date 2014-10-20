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
  $('.registration-form-wrapper input[type="submit"]').one().click(function() {
    var elemName = $(this).siblings('input[name="user"]');
    var elemPass = $(this).siblings('input[name="pass"]');
    var elemRe_pass = $(this).siblings('input[name="re_pass"]');
    var name = $(elemName).val();
    var pass = $(elemPass).val();
    var re_pass = $(elemRe_pass).val();
    if (name.length < 2) {
      $('.error-message').remove();
      $(elemName).before('<div class="error-message">field is required</div>');
      return false;
    }
    if (name.length > 32) {
      $('.error-message').remove();
      $(elemName).before('<div class="error-message">name is too long</div>');
      return false;
    }
    if (pass.length < 2) {
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
      $(elemPass).before('<div class="error-message">passwords must match</div>');
      return false;
    }
  });


  $('.login-form-wrapper input[type="submit"]').one().click(function() {
    var elemName = $(this).siblings('input[name="user"]');
    var elemPass = $(this).siblings('input[name="pass"]');

    var name = $(elemName).val();
    var pass = $(elemPass).val();

    if (name.length < 2) {
      $('.error-message').remove();
      $(elemName).before('<div class="error-message">field is required</div>');
      return false;
    }
    if (name.length > 32) {
      $('.error-message').remove();
      $(elemName).before('<div class="error-message">name is too long</div>');
      return false;
    }
    if (pass.length < 2) {
      $('.error-message').remove();
      $(elemPass).before('<div class="error-message">field is required</div>');
      return false;
    }
    if (pass.length > 32) {
      $('.error-message').remove();
      $(elemPass).before('<div class="error-message">password is too long</div>');
      return false;
    }


    var login_form = $.post("/login"
      ,{
        user: name,
        pass: pass
      }
      , function(data) {
        if ("success" in data){
            location.reload(true);// <!-- relocate to home  -->
        }
        else {
            var mes = "Other error";
            if ("error" in data)  mes = data["error"];
            $('.error-message').remove();
            $(elemPass).before('<div class="error-message">' + mes + '</div>');
        }
      }
      , "json"
    );

    login_form.fail(
        function() {
            var mes = "";
            $('.error-message').remove();
            $(elemPass).before('<div class="error-message">Request error</div>');
        }
    );
    return false;

  });
});
