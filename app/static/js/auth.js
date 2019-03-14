$("#register-button").on("click", function(e) {
  e.preventDefault();

  var gender;
  if ($('input[id=female]:checked').val() == 'on') {
    gender = "Female"}
  else {
    gender = "Male"}

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
    sex_pref: $("#sex_pref").val(),
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
    login: $('#my-login').val(),
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
      if (res.fields) {
          res.fields.forEach(function(item) {
          $("input[id=" + item + "]").addClass("error");
        });
      }
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

function getLocation(href) {
    var match = href.match(/^(https?\:)\/\/(([^:\/?#]*)(?:\:([0-9]+))?)([\/]{0,1}[^?#]*)(\?[^#]*|)(#.*|)$/);
    return match && {
        href: href,
        protocol: match[1],
        host: match[2],
        hostname: match[3],
        port: match[4],
        pathname: match[5],
        search: match[6],
        hash: match[7]
    }
}

$("#recovery-button").on('click', function (e) {
    e.preventDefault();

    var url = getLocation(location.href);
    var search = url['search'];
    var email = search.match(/\?email=(\w+\@\w+.\w+)/)[1];
    var token = search.match(/\&token=(\w+)/)[1];

    // console.log(email);
    // console.log(token);

    var data = {
        email: email,
        token: token,
        new_password: $("#new_password").val(),
        confirm_password: $("#confirm_password").val()
    };

    $.ajax({
        type: "POST",
        data: data,
        url: "/ajax_recovery"
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