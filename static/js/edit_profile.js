window.addEventListener('load', () => {

    let closeTimeout;

    $('.edit-profile-edit-img').on('click', (e) => {
        let field = e.target.id.replace('edit-', '');
        let data = $(`#data-${field}`).html();
        $('.edit-profile-submit').attr('id', field);
        if(field == 'description') {
            $('.edit-profile-textarea').css('display', 'block');
            $('.edit-profile-textarea').val(data);
        } else if(field == 'birthdate') {
            $('.datepicker').val($('#user_birthdate').val());
            $('.datepicker').datepicker("option", "defaultDate", $('#user_birthdate').val());
            $('.datepicker').css('display', 'block');
        } else if(field == 'field_of_activity') {
            $('#edit-fake-select').css('display', 'block');
            $('.register-selected').attr('id', `selected-${$('.user_field_of_activity').val()}`);
            $('.register-selected').html($('.data-field_of_activity').val());
        } else {
            let input = $('.edit-profile-input');
            input.css('display', 'block');
            input.val(data);
            if(field == 'photo') {
                input.attr('type', 'file');
            } else {
                let label = $(`#label-${field}`).html().replace(': ', '');
                input.attr('placeholder', label);
                input.attr('type', 'text');
            }
        }

        $('.faq-background').css('display', 'flex');
    })

    $('.edit-profile-submit').on('click', (e) => {
        const token = $('input[name=csrfmiddlewaretoken]').val();
        let field = e.target.id;
        let input = field == 'description' ? $('.edit-profile-textarea') : $('.edit-profile-input');
        if(field == 'birthdate') {
            input = $('.datepicker');
        }
        let newValue;
        if(field == 'field_of_activity') {
            newValue = $('.register-selected').attr('id').replace('selected-', '');
        } else {
            newValue = input.val();
        }
        let validated = true;

        if(field == 'email' && !/^[a-zA-Z0-9-_\.]+@[a-zA-Z0-9-_]+\.[a-zA-Z0-9-_]+$/.test(newValue)) {
            validated = false;
            input.addClass('wrong-input');
        }
        if(field == 'phone_number' && !/^[0-9\+]+$/.test(newValue)) {
            validated = false;
            input.addClass('wrong-input');
        }

        if(newValue && validated) {
            let formData = new FormData();
            formData.append('csrfmiddlewaretoken', token);
            formData.append('g-recaptcha-response', $('#g-recaptcha-response').val());
            formData.append('field', field);
            formData.append('new_value', newValue);
            if(field == 'photo') {
                formData.append('photo', $('.edit-profile-input').prop('files')[0])
            }
            $.ajax({
                method: "post",
                url: "/authentication/edit_profile/",
                contentType: false,
                processData: false,
                data: formData,
                success: (data) => {
                    let notificationText = '';
                    if(data['result'] == 'ok') {
                        notificationText = 'Заявка на изменение данных профиля отправлена успешно';
                        $('.faq-form-notification').css('margin-bottom', '');
                        $('.faq-background-form-content').css('display', 'none');
                        if(Object.keys(data).includes('pk')) {
                            $(`.application-${field}`).remove();
                            if($('.edit-profile-rejected-block').children().length == 0) {
                                $('.edit-profile-rejected-wrapper').css('display', 'none');
                            }
                            let pk = data['pk'];
                            let htmlString = `<div class="edit-profile-application application-${field}" id="application-${pk}">
                            <div class="edit-profile-application-left">
                                <span class="specialists-info-label">${data['verbose_field']}: </span>`;
                            if(field == 'photo') {
                                htmlString += `<div class="specialists-img-block">
                                        <img src="/media/${data['new_value']}" alt="photo" class="specialists-img">
                                    </div>`;
                            } else if(field == 'field_of_activity') {
                                htmlString += `<span class="edit-profile-application-value">${data['new_value'].replace(/id:[0-9]\|/, '')}</span>`;
                            } else {
                                htmlString += `<span class="edit-profile-application-value">${newValue}</span>`;
                            }
                            htmlString += `</div><div class="med-button mini-med-button edit-profile-application-delete" id="application-delete-${pk}">Удалить</div></div>`;
                            $('.edit-profile-waiting-block').prepend(htmlString);
                            $('.edit-profile-waiting-wrapper').css('display', 'flex');
                        }
                        closeTimeout = window.setTimeout(() => {
                            $('.faq-background').click();
                        }, 5000);
                    } else if(data['result'] == 'captcha') {
                        notificationText = 'Капча не пройдена';
                        $('.faq-form-notification').css('margin-bottom', '15px');
                    } else if(data['result'] == 'email') {
                        notificationText = 'Пользователь с этим адресом электронной почты уже существует';
                        $('.faq-form-notification').css('margin-bottom', '15px');
                    } else if(data['result'] == 'failed') {
                        notificationText = 'Упс, что-то пошло не так. Попробуйте позже :с';
                        $('.faq-form-notification').css('margin-bottom', '15px');
                    }
                    $('.faq-form-notification').html(notificationText);
                },
                error: (data) => {
                }
            });
        }
    })

    $(document).on('click', '.edit-profile-application-delete', (e) => {
        const token = $('input[name=csrfmiddlewaretoken]').val();
        let pk = e.target.id.replace('application-delete-', '');
        $.ajax({
            method: "post",
            url: "/authentication/delete_application/",
            data: {csrfmiddlewaretoken: token, pk: pk},
            success: (data) => {
                if($('.edit-profile-waiting-block').children().length == 1) {
                    $('.edit-profile-waiting-wrapper').css('display', 'none');
                }
                $(`#application-${pk}`).remove();
            },
            error: (data) => {
            }
        });
    })

    $('.faq-background').on('click', (e) => {
        if(e.target.classList.contains('faq-background')) {
            e.target.style.display = '';
            let input = $('.edit-profile-input');
            let textarea = $('.edit-profile-textarea');
            input.css('display', '');
            input.val('');
            input.removeAttr('placeholder');
            input.attr('type', 'text');
            textarea.css('display', '');
            textarea.val('');
            $('.datepicker').css('display', '');
            $('#edit-fake-select').css('display', '');
            $('.edit-profile-submit').removeAttr('id');
            $('.wrong-input').removeClass('wrong-input');
            grecaptcha.reset();
            $('.faq-form-notification').html('');
            $('.faq-form-notification').css('margin-bottom', '');
            $('.faq-background-form-content').css('display', '');
            window.clearTimeout(closeTimeout);
        }
    })

    $('.register-fake-select').on('click', (e) => {
        if($('.register-options-block').css('display') == 'flex') {
            $('.register-options-block').css('display', '');
        } else {
            $('.register-options-block').css('display', 'flex');
        }
    });

    $(document).on('click', '.register-option', (e) => {
        let id = e.target.id.replace('option-', 'selected-');
        $('.register-selected').attr('id', id);
        $('.register-selected').html(e.target.innerHTML);
    })

    $('.datepicker').datepicker({
        changeMonth: true,
        changeYear: true,
        yearRange: "c-100:c+0",
        dateFormat: "dd-mm-yy",
        defaultDate: $('#data_birthdate').html()
    });

    $('.datepicker').on('focus', () => {
        $('.datepicker').prop( "disabled", true );
    })

    $('.datepicker').on('blur', (e) => {
        $('.datepicker').prop( "disabled", false );
    })
})