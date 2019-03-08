$('#search').on('click', function (e) {
    e.preventDefault();

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
        interest4 = $('#interest4').val();

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
        'interest4': interest4
    };

    $.ajax({
        type: 'POST',
        data: data,
        url: '/ajax_search'
    });
    //     .done(function (data) {
    //     var res = JSON.parse(data);
    //     if (res.ok == false) {
    //         // $('#message_search')
    //         console.log('false');
    //     } else {
    //         console.log('true');
    //     }
    // });
    console.log(data);

});
