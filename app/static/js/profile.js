$("#edit-button").on('click', function (e) {
  e.preventDefault();

  var data = {
    my_password: $("#my-password").val(),
    new_password: $("#new-password").val(),
    confirm_password: $("#confirm-password").val()
  };

  console.log(data);
  $.ajax({
      type: "POST",
      data: data,
      url: "/profile/edit/password"
  }).done(function(data) {
    var res = JSON.parse(data);
    if (res.ok == false) {
      console.log(res.error);
      $("#message-edit").text("");
      $("#message-edit").text(res.error);
    } else {
      $("#message-edit").text("");
      $("#message-edit").text(res.error);
    }
  });
});