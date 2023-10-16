window.addEventListener('load', () => {

    $('.edit-profile-edit-img').on('click', (e) => {
        let field = e.target.id.replace('edit-', '');
        let data = $(`#data-${field}`).html();
        $('.edit-profile-submit').attr('id', field);
        if(field == 'description') {
            $('.edit-profile-textarea').css('display', 'block');
            $('.edit-profile-textarea').val(data);
        } else if(field == 'birthdate') {
            console.log()
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
                    if(data['result'] == 'ok') {

                    } else if(data['result'] == 'captcha') {

                    } else if(data['result'] == 'email') {
                        
                    } else if(data['result'] == 'failed') {
                        
                    }
                },
                error: (data) => {
                }
            });
        }
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