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
      console.log(res)
        if (res.ok == false) {
          $("#message-edit").text("");
          $("#message-edit").text(res.error)
          if (res.fields) {
            res.fields.forEach(function (item) {
                $("input[name=" + item + "]").addClass("error");
            });
          } else {
            $("#message-edit").text("");
            $("#message-edit").text(res.error());
          }
        }
    });
});


// $("#edit-button").on('click', function (e) {
//   e.preventDefault();
//
//   var data = {
//     my_password: $("#my_password").val(),
//     new_password: $("#new_password").val(),
//     confirm_password: $("#confirm_password").val()
//   };
//
//   console.log(data);
//   $.ajax({
//       type: "POST",
//       data: data,
//       url: "/profile/edit/password"
//   }).done(function(data) {
//     var res = JSON.parse(data);
//     console.log(1)
//     if (res.ok == false) {
//       console.log(res.error);
//       $("#message-edit").text("");
//       $("#message-edit").text(res.error);
//       if (res.fields) {
//         res.fields.forEach(function(item) {
//           $("input[name=" + item + "]").addClass("error");
//         });
//       }
//     } else {
//       $("#message-edit").text("");
//       $("#message-edit").text(res.error);
//     }
//   });
// });
