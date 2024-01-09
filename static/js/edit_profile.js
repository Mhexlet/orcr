window.addEventListener('load', () => {

    let closeTimeout;

    let croppie = $('.edit-profile-photo').croppie({
        enableExif: true,
        viewport: {
            width: 250,
            height: 250
        }
    });

    $('.summernote').summernote({
        height: 120,
        lang: "ru-RU",
        placeholder: "О себе",
        toolbar: [
            ['style', ['style']],
            ['font', ['bold', 'underline', 'clear']],
            ['fontname', ['fontname']],
            ['color', ['color']],
            ['para', ['ul', 'ol', 'paragraph']],
            ['insert', ['link']],
            ['view', ['fullscreen', 'codeview', 'help']],
        ],
    });

    $('#data-field_of_activity > p').each((i, foa) => {
        $(`#${foa.id.replace('foa', 'option')}`).addClass('selected');
    })

    $('.edit-profile-edit-img').on('click', (e) => {
        let field = e.target.id.replace('edit-', '');
        let data = $(`#data-${field}`).html();
        $('.edit-profile-submit').attr('id', field);
        if(field == 'description') {
            $('.note-editor').css('display', 'block');
            $('.summernote').summernote('code', data);
        } else if(field == 'birthdate') {
            let input = $('.edit-profile-date-input');
            input.css('display', 'flex');
            input.val($('#birthdate-hidden').val());
        } else if(field == 'photo') {
            $('.edit-profile-photo-input').attr('style', 'display: flex !important');
        } else if(field == 'field_of_activity') {
            $('#edit-fake-select').css('display', 'block');
        } else {
            let input = $('.edit-profile-input');
            input.css('display', 'block');
            input.val(data);
            let label = $(`#label-${field}`).html().replace(': ', '');
            input.attr('placeholder', label);
        }

        $('.faq-background').css('display', 'flex');
    })

    $('.edit-profile-photo-input').on('change', (e) => {
        $('.edit-profile-photo-block').css('display', 'flex');
        let reader = new FileReader();

        reader.onload = function(e) {
            croppie.croppie('bind', {url: e.target.result});
        };

        reader.readAsDataURL(e.target.files[0]);
    })

    $('.register-option').on('click', (e) => {
        if(e.target.classList.contains('selected')) {
            e.target.classList.remove('selected');
        } else {
            e.target.classList.add('selected');
        }
    })

    function editAjax(formData, action, field, newValue) {
        $.ajax({
            method: "post",
            url: `/authentication/${action}/`,
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
                            htmlString += `<span class="edit-profile-application-value">${data['new_value']}</span>`;
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

    $('.edit-profile-submit').on('click', (e) => {
        const token = $('input[name=csrfmiddlewaretoken]').val();
        let field = e.target.id;
        let input = $('.edit-profile-input');
        if(field == 'birthdate') {
            input = $('.edit-profile-date-input');
        } else if(field == 'photo') {
            input = $('#cropped-photo');
        }
        let newValue;
        if(field == 'field_of_activity') {
            newValue = []
            $('.register-option.selected').each((i, option) => {
                newValue.push(option.id.replace('option-', ''));
            })
        } else if(field == 'photo') {
            newValue = true;
        } else if(field == 'description') {
            newValue = $('.note-editable').html();
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
            if(field == 'field_of_activity') {
                formData.append('new_value', JSON.stringify(newValue));
                editAjax(formData, 'edit_foas', field, newValue);
            } else {
                formData.append('new_value', newValue);
                if(field == 'photo') {
                    croppie.croppie('result', {
                        type: 'blob',
                        format: 'jpeg',
                        size: 'original'
                    }).then(function (blob) {
                        const file = new File([blob], "fileName.jpg", { type: "image/jpeg" });
                        formData.append('photo', file)
                        editAjax(formData, 'edit_profile', field, newValue);
                    });
                } else {
                    editAjax(formData, 'edit_profile', field, newValue);
                }
            }
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
            input.css('display', '');
            input.val('');
            input.removeAttr('placeholder');
            $('.note-editor').css('display', '');
            $('.summernote').val('');
            $('.edit-profile-date-input').css('display', '');
            $('.edit-profile-photo-block').css('display', '');
            $('.edit-profile-photo-input').css('display', '');
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

    // $('.datepicker').datepicker({
    //     changeMonth: true,
    //     changeYear: true,
    //     yearRange: "c-100:c+0",
    //     dateFormat: "dd-mm-yy",
    //     defaultDate: $('#data_birthdate').html()
    // });

    // $('.datepicker').on('focus', () => {
    //     $('.datepicker').prop( "disabled", true );
    // })

    // $('.datepicker').on('blur', (e) => {
    //     $('.datepicker').prop( "disabled", false );
    // })
})