// $('#add_comment').on('click', function (e) {
//     e.preventDefault();
//     console.log('blah');
//     data = {
//         id_photo: $('#id_photo').val(),
//         text: $('#comment').val()
//     };
//
//     console.log(data);
//
//     // $.ajax({
//     //     type: 'POST',
//     //     data: data,
//     //     url: '/ajax_add_comment'
//     // }).done(function (data) {
//     //     var res = JSON.parse(data);
//     //     if (res.ok == false) {
//     //         console.log(res.error)
//     //     } else {
//     //         console.log(res.error)
//     //     }
//     // });
//
// });

function add_comment(id_photo) {
    data = {
        id_photo: id_photo,
        text: $('#comment').val()
    };

    $.ajax({
        type: 'POST',
        data: data,
        url: '/ajax_add_comment'
    }).done(function (data) {
        console.log('blah');
        var res = JSON.parse(data);
        if (res.ok == false) {
            console.log(res.error);
        } else {
            console.log(res.error);
        }
    });
}