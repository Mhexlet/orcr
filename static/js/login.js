window.addEventListener('load', () => {

    if($('#id_username').val()) {
        $('.login-form').after('<div class="faq-form-notification">Логин или пароль введены неверно</div>')
    }

    $('.med-input').on('blur', (e) => {
        if(!e.target.value) {
            e.target.classList.add('wrong-input');
        } else {
            e.target.classList.remove('wrong-input');
        }
    })

    $('.login-password-show').on('click', () => {
        $('.login-password-show').css('display', 'none');
        $('.login-password-hide').css('display', 'block');
        $('#id_password').attr('type', 'text');
    })

    $('.login-password-hide').on('click', () => {
        $('.login-password-show').css('display', '');
        $('.login-password-hide').css('display', '');
        $('#id_password').attr('type', 'password');
    })

    $('.login-submit').on('click', (e) => {
        let validated = true;

        $('.med-input').each((i, input) => {
            if(!input.value) {
                validated = false;
                input.classList.add('wrong-input');
            }
        })

        if(!validated) {
            e.preventDefault();
        }
    })

})