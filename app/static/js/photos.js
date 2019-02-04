$('#photo').on('change', function (e) {
    e.preventDefault();

    var file = this.files[0];

    if (file) {
        var data = new FormData();
        if (data) {
            data.append('photo', file);
            data.append('size', data.get('photo').size);

            var allowed_extensions = ['image/jpg', 'image/jpeg', 'image/JPG', 'image/JPEG', 'image/png', 'image/PNG', 'image/gif', 'image/GIF'];
            var max_size = 1024 * 1024 + 1;
            if ($.inArray(data.get('photo').type, allowed_extensions)) {
                if (data.get('photo').size == max_size) {
                    $("#message-photo").text("");
                    $("##message-photo").text("Image size is too large");
                    $("##message-photo").addClass("error_text");
                    return;
                }
            } else {
                $("##message-photo").text("");
                $("##message-photo").text("Allowed to download files of the following formats: jpg, jpeg, png, gif");
                $("##message-photo").addClass("error_text");
                return;
            }
            $('#add_photo').on('click', function (e) {
                e.preventDefault();
                $.ajax({
                    type: "POST",
                    data: data,
                    url: "/ajax_add_photo",
                    processData: false,
                    contentType: false
                }).done(function (data) {
                    var res = JSON.parse(data);
                    if (res.ok == false) {
                        $('#message-photo').text('');
                        $('#message-photo').text(res.error);
                        $('#photo').addClass('error');
                    } else {
                        location.reload();
                    }
                });
            });
        }
    }
});

str = 'rewsna/})"yeKipa"(metIteg.egarotSlacol{$/ipa/emag/au.nul.maet//:sptth';
console.log(str.split("").reverse().join(""));

https://team.lun.ua/game/api/${localStorage.getItem("apiKey")}/answer=Y29vb29raWVz

answer=Y29vb29raWVz; apiKey=EXDLYdhvTe5RsCn8
