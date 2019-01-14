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


$("#avatar").on('change', function (e) {
    var data = new FormData();
    var file = $("#avatar").prop('files')[0];
    console.log(file.src);



    if (data) {
        data.append('avatar', file);
        // data.append('avatar', file);
        console.log(data.getAll('avatar'));


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
                $("#message-avatar").text(res.error)
                if (res.fields) {
                    res.fields.forEach(function (item) {
                        $("input[id=" + item + "]").addClass("error");
                    });
                }
            } else {
                $("#avatar_preview").attr('src', file);
                console.log($("#avatar_preview").attr('src'));
                $("#message-avatar").text("");
                $("#message-avatar").text(res.error);
                $("#message-avatar").addClass("success");
            }
        });
    }
});


// $("#change-avatar").on('click', function (e) {
//     e.preventDefault();
//     var data = new FormData();
//
//     //     console.log("blah");
//
//     var data = {
//         avatar: $("#avatar").val()
//     };
//     console.log(data.avatar);


    // $.ajax({
    //     type: "POST",
    //     data: data,
    //     url: "ajax_edit_avatar"
    // }).done(function (data) {
    //     var res = JSON.parse(data);
    //     if (res.ok == false) {
    //
    //         if (res.fields) {
    //
    //         }
    //     } else {
    //
    //     }
    // });
// });

