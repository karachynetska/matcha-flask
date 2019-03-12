function search() {
    $('#found_users').empty();

    var first_name = $('#first_name').val(),
        last_name = $('#last_name').val(),
        from_age = $('#from_age').val(),
        to_age = $('#to_age').val(),
        from_rate = $('#from_rate').val(),
        to_rate = $('#to_rate').val(),
        gender = $('#gender').val(),
        country = $('#country').val(),
        city = $('#city').val(),
        interest1 = $('#interest1').val(),
        interest2 = $('#interest2').val(),
        interest3 = $('#interest3').val(),
        interest4 = $('#interest4').val(),
        filter = $('#filter').val(),
        sort = $('#sort').val();

    var data = {
        'first_name': first_name,
        'last_name': last_name,
        'from_age': from_age,
        'to_age': to_age,
        'from_rate': from_rate,
        'to_rate': to_rate,
        'gender': gender,
        'country': country,
        'city': city,
        'interest1': interest1,
        'interest2': interest2,
        'interest3': interest3,
        'interest4': interest4,
        'filter': filter,
        'sort': sort
    };
    console.log(data);

    $.ajax({
        type: 'POST',
        data: data,
        url: '/ajax_search'
    }).done(function (data) {
        var res = JSON.parse(data);
        if (res.ok == true) {
            if (res.found_users) {
                jQuery.each(res.found_users, function (i, val) {
                    $('#found_users').append('<div class="friend-card">\n' +
                       '                      <img src="'+val['background']+'" alt="profile-cover" class="img-responsive cover" />\n' +
                       '                      <div class="card-info">\n' +
                       '                        <img src="'+val['avatar']+'" alt="user" class="profile-photo-lg" />\n' +
                       '                        <div class="friend-info">\n' +
                       '                          <h5><a href="/profile/id'+val['id']+'" class="profile-link">'+val['firstname']+ ' ' + val['lastname']+'</a></h5>\n' +
                       '                          <p>'+val['login']+'</p>\n' +
                       '                        </div>\n' +
                       '                      </div>\n' +
                       '                    </div>')
                });
                $('#filter_sort').removeClass('none');
            }
        } else {
            $('#found_users').append('<h3>'+res.error+'</h3>');
        }
    });
}
$('#search').on('click', function (e) {
    e.preventDefault();
    search();
});

$('#filter').on('change', function (e) {
    e.preventDefault();
    search();
});

$('#sort').on('change', function (e) {
    e.preventDefault();
    search();
});
