$("#register-button").on("click", function(e) {
  e.preventDefault();

  var data = {
    firstname: $("#firstname").val(),
    lastname: $("#lastname").val(),
    login: $("#rlogin").val(),
    email: $("#email").val(),
    password: $("#password").val(),
    day: $("#day").val(),
    month: $("#month").val(),
    year: $("#year").val(),
    gender: $("#gender"),
    city: $("#city").val(),
    country: $("#country").val()
  };

  $.ajax({
    type: "POST",
    data: JSON.stringify(data),
    contentType: "application/json",
    url: "/register"
  }).done(function(data) {
    if (!data.ok) {
      $("#message-register").text("");
      $("#message-register").text(data.error);
      if (data.fields) {
        data.fields.forEach(function(item) {
          $("input[name=" + item + "]").addClass("error");
        });
      }
    } else {
      $("#message-register").text(
        "Registration completed successfully. Please check your email."
      );
    }
  });
});