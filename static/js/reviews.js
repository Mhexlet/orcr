window.addEventListener('load', () => {

    let closeTimeout;

    function closeBackground() {
        $('.faq-background').css('display', '');
        $('.faq-question-input').css('display', '');
        $('.faq-name-input').css('display', '');
        $('.faq-form-submit').css('display', '');
        $('.faq-question-input').val('');
        $('.faq-name-input').val('');
        $('.faq-form-notification').html('');
        $('.g-recaptcha').css('display', '');
        $('.faq-form-notification').css('margin-bottom', '');
        window.clearTimeout(closeTimeout);
        $('.wrong-input').removeClass('wrong-input');
    }

    $('.faq-ask-question').on('click', () => {
        grecaptcha.reset();
        $('.faq-background').css('display', 'flex');
    })

    $('.faq-form-submit').on('click', () => {
        const token = $('input[name=csrfmiddlewaretoken]').val();
        let name = $('.faq-name-input').val();
        let text = $('.faq-question-input').val();

        let validated = true;
        $('.wrong-input').removeClass('wrong-input');
        if(!name || name.length > 64) {
            validated = false;
            $('.faq-name-input').addClass('wrong-input');
        }
        if(!text) {
            validated = false;
            $('.faq-question-input').addClass('wrong-input');
        }
        if(validated) {
            $.ajax({
                method: "post",
                url: "/create_review/",
                data: {csrfmiddlewaretoken: token, 'g-recaptcha-response': $('#g-recaptcha-response').val(), name: name, text: text},
                success: (data) => {
                    let notificationText = '';
                    if(data['result'] == 'ok') {
                        notificationText = 'Ваш отзыв успешно отправлен!';
                        $('.faq-question-input').css('display', 'none');
                        $('.faq-name-input').css('display', 'none');
                        $('.faq-form-submit').css('display', 'none');
                        $('.g-recaptcha').css('display', 'none');
                        $('.faq-form-notification').css('margin-bottom', '');
                        closeTimeout = window.setTimeout(() => {
                            closeBackground();
                        }, 5000);
                    } else if(data['result'] == 'captcha') {
                        notificationText = 'Капча не пройдена';
                        $('.faq-form-notification').css('margin-bottom', '15px');
                    } else {
                        notificationText = 'Упс, что-то пошло не так. Попробуйте позже :с';
                        $('.faq-form-notification').css('margin-bottom', '15px');
                    }
                    $('.faq-form-notification').css('display', 'inline');
                    $('.faq-form-notification').html(notificationText);
                },
                error: (data) => {
                }
            });
        }
    })

    $('.faq-background').on('click', (e) => {
        if(e.target.classList.contains('faq-background')) {
            closeBackground();
        }
    })

    $(document).on('keydown', (e) => {
        let type = e.code;
        if(type == 'ArrowLeft') {
            $('.paginator-previous').click();
        } else if(type == 'ArrowRight') {
            $('.paginator-next').click();
        }
    });
})