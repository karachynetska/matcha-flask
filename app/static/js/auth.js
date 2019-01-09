$("#register-button").on("click", function(e) {
  e.preventDefault();

  var gender;
  if ($('input[id=female]:checked').val() == 'on') {
    gender = "female"}
  else {
    gender = "male"}

  var data = {
    firstname: $("#firstname").val(),
    lastname: $("#lastname").val(),
    login: $("#rlogin").val(),
    email: $("#email").val(),
    password: $("#password").val(),
    day: $("#day").val(),
    month: $("#month").val(),
    year: $("#year").val(),
    gender,
    city: $("#city").val(),
    country: $("#country").val(),
  };

  $.ajax({
    type: "POST",
    data: data,
    url: "/register"
  }).done(function(data) {
    var res = JSON.parse(data);
    if (res.ok == false) {
      $("#message-register").text("");
      $("#message-register").text(res.error);
      if (res.fields) {
        res.fields.forEach(function(item) {
          $("input[id=" + item + "]").addClass("error");
        });
      }
    } else {
      $("#message-register").text(
        "Registration completed successfully. Please check your email."
      );
      $("#message-register").addClass("success");
    }
  });
});

$("#login-button").on('click', function (e) {
  e.preventDefault();

  var data = {
    email: $('#my-email').val(),
    password: $('#my-password').val()
  };

  // console.log(data['email']);
  // console.log(data['password']);

  $.ajax({
      type: "POST",
      data: data,
      url: "/login"
  }).done(function(data) {
    console.log(data);
    var res = JSON.parse(data);
    if (res.ok == false) {
      console.log(res.error);
      $("#message-login").text("");
      $("#message-login").text(res.error);
    } else {
      location.replace('/profile');
    }
  });
});

$("#send-button").on('click', function (e) {
    e.preventDefault();

    var data = {
      email: $("#my-email").val()
    };

    $.ajax({
        type: "POST",
        data: data,
        url: "/ajax_forgot"
    }).done(function (data) {
        var res = JSON.parse(data);
        if (res.ok == false) {
          $("#message-forgot").text("");
          $("#message-forgot").text(res.error);
          if (res.fields) {
                res.fields.forEach(function(item) {
                    $("input[id=" + item + "]").addClass("error");
                });
            }
        } else {
          $("#message-forgot").text("");
          $("#message-forgot").text(res.error);
          $("#message-forgot").addClass("success");
        }
    });
});

$("#recovery-button").on('click', function (e) {
    e.preventDefault();

    var data = {
        new_password: $("#new_password").val(),
        confirm_password: $("#confirm_password").val()
    };

    $.ajax({
        type: "POST",
        data: data,
        url: "/recovery"
    }).done(function (data) {
        var res = JSON.parse(data);
        if (res.ok == false) {
            $("#message-recovery").text("");
            $("#message-recovery").text(res.error);
            if (res.fields) {
                res.fields.forEach(function(item) {
                    $("input[id=" + item + "]").addClass("error");
                });
            }
        } else {
            $("#message-recovery").text("");
            $("#message-recovery").text(res.error);
            $("#message-recovery").addClass("success");
        }
    });
});