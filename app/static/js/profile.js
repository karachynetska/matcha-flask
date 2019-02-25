$("#edit-password").on('click', function (e) {
    e.preventDefault();

    var data = {
      my_password: $("#my_password").val(),
      new_password: $("#new_password").val(),
      confirm_password: $("#confirm_password").val()
    };

    $.ajax({
        type: "POST",
        data: data,
        url: "/ajax_edit_password"
    }).done(function (data) {
        var res = JSON.parse(data);
        if (res.ok == false) {
          $("#message-edit").text("");
          $("#message-edit").text(res.error);
          if (res.fields) {
            res.fields.forEach(function (item) {
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

$("#edit-basic").on('click', function (e) {
    e.preventDefault();

      var gender;
      if ($('input[id=female]:checked').val() == 'on') {
          gender = "female"}
      else if ($('input[id=male]:checked').val() == 'on') {
          gender = "male"}
      else {
          gender = null;
      }
    var data = {
        firstname: $('#firstname').val(),
        lastname: $('#lastname').val(),
        email: $('#email').val(),
        gender,
        sex_pref: $('#sex_pref').val(),
        city: $('#city').val(),
        country: $('#country').val(),
        information: $('#my-info').val()
    };
      console.log(data);

    $.ajax({
        type: "POST",
        data: data,
        url: "/ajax_edit_basic"
    }).done(function (data) {
        var res = JSON.parse(data);
        if (res.ok == false) {
            $("#message-basic").text("");
            $("#message-basic").text(res.error);
            if (res.fields) {
                res.fields.forEach(function (item) {
                    $("input[id=" + item + "]").addClass("error");
                });
            }
        } else {
            $("#message-basic").text("");
            $("#message-basic").text(res.error);
            $("#message-basic").addClass("success");
        }
    });
});


$("#avatar").on('change', function () {
    var file = this.files[0];

    if (file) {
        var data = new FormData();
        if (data) {
            data.append('avatar', file);
            data.append('size', data.get('avatar').size);

            var allowed_extensions = ['image/jpg', 'image/jpeg', 'image/JPG', 'image/JPEG', 'image/png', 'image/PNG', 'image/gif', 'image/GIF'];
            var max_size = 1024 * 1024 + 1;
            if ($.inArray(data.get('avatar').type, allowed_extensions)) {
                if (data.get('avatar').size == max_size) {
                    $("#message-avatar").text("");
                    $("#message-avatar").text("Image size is too large");
                    $("#message-avatar").addClass("error_text");
                    return;
                }
            } else {
                $("#message-avatar").text("");
                $("#message-avatar").text("Allowed to download files of the following formats: jpg, jpeg, png, gif");
                $("#message-avatar").addClass("error_text");
                return;
            }
            var reader = new FileReader();
            reader.onload = function (e) {
                $('#avatar_preview').attr('src', e.target.result);
            }
            reader.readAsDataURL(file);
            $("#message-avatar").text("");
            $("#message-avatar").text("Avatar succesfully uploaded");
            $("#message-avatar").addClass("success");
            $('#change-avatar').on('click', function (e) {
                e.preventDefault();
                $.ajax({
                    type: "POST",
                    data: data,
                    url: "/ajax_edit_avatar",
                    processData: false,
                    contentType: false
                }).done(function (data) {
                    var res = JSON.parse(data);
                    if (res.ok == false) {
                        $("#message-avatar").text("");
                        $("#message-avatar").text(res.error);
                        if (res.fields) {
                            res.fields.forEach(function (item) {
                                $("input[id=" + item + "]").addClass("error");
                            });
                        }
                    } else {
                        location.reload();
                    }
                });
            });
        }
    }
});


$("#add_interest").on('click', function (e) {
    e.preventDefault();

    var data = {
        interest: $("#interest").val()
    };

    console.log(data);

    $.ajax({
        type: "POST",
        data: data,
        url: "/ajax_edit_interests"
    }).done(function (data) {
        var res = JSON.parse(data);
        if (res.ok == false) {
            $('#message-interests').text("");
            $('#message-interests').addClass('error_text');
            $('#message-interests').text(res.error);
            setTimeout(function () {
                $('#message-interests').text('');
            }, 2000);
        } else {
            $('.interests').append('<li id="'+ res.id_interest +'"><a class="tag" style="text-decoration:none"><i class="'+ res.icon +'"></i> '+res.interest+'</a>&nbsp;&nbsp;&nbsp;<a style="cursor: pointer"><i class="ion-android-close"></i></a></li>');
        }
    });
});


function delete_interest(id_interest) {
    var data = {
        'id_interest': id_interest
    };

    $.ajax({
        type: "POST",
        data: data,
        url: '/ajax_delete_interest'
    }).done(function (data) {
        var res = JSON.parse(data);
        if (res.ok == true) {
            $('#'+id_interest).remove();
        } else {
            $('#message-interests').text('');
            $('#message-interests').addClass('error_text');
            $('#message-interests').text(res.error);
            setTimeout(function () {
                $('#message-interests').text('');
            }, 2000);
        }
    });
}

