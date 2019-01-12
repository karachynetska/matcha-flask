$("#edit-button").on('click', function (e) {
    e.preventDefault();

    var data = {
      my_password: $("#my_password").val(),
      new_password: $("#new_password").val(),
      confirm_password: $("#confirm_password").val()
    };

    console.log(data);
    $.ajax({
        type: "POST",
        data: data,
        url: "/ajax_edit_password"
    }).done(function (data) {
      console.log("blah")
        var res = JSON.parse(data);
      // console.log(res.fields);
        if (res.ok == false) {
          $("#message-edit").text("");
          $("#message-edit").text(res.error)
          if (res.fields) {
            res.fields.forEach(function (item) {
                console.log(item);
                $("input[id=" + item + "]").addClass("error");
            });
          }
        } else {
            $("#message-edit").text("");
            $("#message-edit").text(res.error);
            $("#message-edit").addClass("success");
        }
    });
});

$("#change-avatar").on('click', function (e) {
    e.preventDefault();

    var data = {
        avatar: $("#avatar").val();
    };

    $.ajax({
        type: "POST",
        data: data,
        url: "/profile/edit/avatar"
    }).done(function (data) {
        var res = JSON.parse(data);
        if (res.ok == false) {

            if (res.fields) {

            }
        } else {

        }
    });
});

