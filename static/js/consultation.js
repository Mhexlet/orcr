window.addEventListener('load', () => {

    let closeTimeout;

    $('.consultation-email').on('blur', (e) => {
        if(!/^[a-zA-Z0-9-_\.]+@[a-zA-Z0-9-_]+\.[a-zA-Z0-9-_]+$/.test(e.target.value)) {
            e.target.classList.add('wrong-input');
        } else {
            e.target.classList.remove('wrong-input');
        }
    });

    $('.consultation-phone-number').on('blur', (e) => {
        if(!/^[0-9\+]+$/.test(e.target.value)) {
            e.target.classList.add('wrong-input');
        } else {
            e.target.classList.remove('wrong-input');
        }
    })

    $('.consultation-submit').on('click', () => {
        const token = $('input[name=csrfmiddlewaretoken]').val();
        let email = $('.consultation-email').val();
        let phoneNumber = $('.consultation-phone-number').val();
        let name = $('.consultation-name').val();
        let surname = $('.consultation-surname').val();
        let patronymic = $('.consultation-patronymic').val();
        let address = $('.consultation-address').val();
        let question = $('.consultation-question').val();

        let validated = true;
        $('.wrong-input').removeClass('wrong-input');
        if(!/^[a-zA-Z0-9-_\.]+@[a-zA-Z0-9-_]+\.[a-zA-Z0-9-_]+$/.test(email) || !email) {
            validated = false;
            $('.consultation-email').addClass('wrong-input');
        }
        if(!/^[0-9\+]+$/.test(phoneNumber) || !phoneNumber || phoneNumber.length > 16) {
            validated = false;
            $('.consultation-phone-number').addClass('wrong-input');
        }
        if(!name || name.length > 64) {
            validated = false;
            $('.consultation-name').addClass('wrong-input');
        }
        if(!surname || surname.length > 64) {
            validated = false;
            $('.consultation-surname').addClass('wrong-input');
        }
        if(!patronymic || patronymic.length > 64) {
            validated = false;
            $('.consultation-patronymic').addClass('wrong-input');
        }
        if(!address) {
            validated = false;
            $('.consultation-address').addClass('wrong-input');
        }
        if(!question) {
            validated = false;
            $('.consultation-question').addClass('wrong-input');
        }
        if(!$('.consultation-checkbox').is(":checked")) {
            validated = false;
            $('.consultation-checkbox-block > span').addClass('wrong-input');
        }

        if(validated) {
            $.ajax({
                method: "post",
                url: "/create_application/",
                data: {csrfmiddlewaretoken: token, 'g-recaptcha-response': $('#g-recaptcha-response').val(), name: name, question: question, surname: surname, 
                patronymic: patronymic, address: address, email: email, phone_number: phoneNumber},
                success: (data) => {
                    let notificationText = '';
                    if(data['result'] == 'ok') {
                        notificationText = 'Ваша заявка успешно отправлена!';
                        $('.med-input').val('');
                        grecaptcha.reset();
                        $('.consultation-checkbox').prop('checked', false);
                    } else if(data['result'] == 'captcha') {
                        notificationText = 'Капча не пройдена';
                    } else {
                        notificationText = 'Упс, что-то пошло не так. Попробуйте позже :с';
                    }
                    $('.faq-form-notification').html(notificationText);
                    $('.faq-background').css('display', 'flex');
                    closeTimeout = window.setTimeout(() => {
                        $('.faq-background').css('display', '');
                    }, 5000);
                    
                },
                error: (data) => {
                }
            });
        }
    })

    $('.faq-background').on('click', (e) => {
        if(e.target.classList.contains('faq-background')) {
            $('.faq-background').css('display', '');
            window.clearTimeout(closeTimeout);
        }
    })
})