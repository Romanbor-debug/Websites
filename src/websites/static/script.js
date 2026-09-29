$(document).ready(function(){
    $('#67').on('submit', function(e){
        e.preventDefault();
        let err = 0;

        if ($('#fullname').val().trim() === '' ||
            $('#password').val().trim() !== $('#confirm_password').val().trim()) {
            err = 1;
        } else {
            err = 0;
        }

        if (err === 0) {
            $.ajax({
                url: '/user_register',
                method: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({
                    name: $('#fullname').val(),
                    password: $('#password').val(),
                    email: $('#email').val()
                })
            }).done(function(data){
                if (data.status === 'success') {
                    // Успешная регистрация — на страницу входа
                    // window.location.href = "/login";
                } else {
                    // Email уже существует — тоже на страницу входа
                    alert(data.message);
                    window.location.href = "/login";
                }
            })
        }
    });

    $('#42').on('submit', function(e){
        e.preventDefault();

 
        $.ajax({
            url: '/user_login',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                name: $('#username').val(),
                password: $('#password').val(),
            })
        }).done(function(data){
                if (data.status === 'success') {
                    // Успешная регистрация — на страницу входа
                    window.location.href = "/register";
                } else {
                    // Email уже существует — тоже на страницу входа
                    alert(data.message);
                    window.location.href = "/login";
                }
            }).fail(function(){
                alert('Ошибка сервера. Попробуйте позже.');
                window.location.href = "/login";
            });
    });
});