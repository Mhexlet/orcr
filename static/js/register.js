window.addEventListener('load', () => {

    let options = '';
    $('#id_field_of_activity > option').slice(1).each((i, option) => {
        options += `<span class="register-option" id="option-${option.value}">${option.innerHTML}</span>`
    })
    $('.register-options-block').append(options);
    if(!$('#id_field_of_activity > option:selected').val()) {
        $('#id_field_of_activity > option:selected').removeAttr('selected');
        $('#id_field_of_activity > option:nth-child(2)').attr('selected', true);
    }
    $('.register-selected').html($('#id_field_of_activity > option:nth-child(2)').html());

    $('.register-fake-select').on('click', (e) => {
        if($('.register-options-block').css('display') == 'flex') {
            $('.register-options-block').css('display', '');
        } else {
            $('.register-options-block').css('display', 'flex');
        }
    });

    $(document).on('click', '.register-option', (e) => {
        let id = e.target.id.replace('option-', '');
        $('#id_field_of_activity > option').removeAttr('selected').filter(`[value=${id}]`).attr('selected', true);
        $('.register-selected').html(e.target.innerHTML);
    })

    $('.datepicker').datepicker({
        changeMonth: true,
        changeYear: true,
        dateFormat: "dd-mm-yy"
    });

    $('.datepicker').on('focus', () => {
        $('.datepicker').prop( "disabled", true );
    })

    $('.datepicker').on('blur', (e) => {
        $('.datepicker').prop( "disabled", false );
    })

    $('.med-input').on('blur', (e) => {
        if(!['id_phone_number', 'id_email', 'register-fake-select', 'id_birthdate'].includes(e.target.id)) {
            if(!e.target.value) {
                e.target.classList.add('wrong-input');
            } else {
                e.target.classList.remove('wrong-input');
            }
        }
    })

    $('#id_email').on('blur', (e) => {
        if(!/^[a-zA-Z0-9-_\.]+@[a-zA-Z0-9-_]+\.[a-zA-Z0-9-_]+$/.test(e.target.value)) {
            e.target.classList.add('wrong-input');
        } else {
            e.target.classList.remove('wrong-input');
        }
    });

    $('#id_phone_number').on('blur', (e) => {
        if(!/^[0-9\+]+$/.test(e.target.value)) {
            e.target.classList.add('wrong-input');
        } else {
            e.target.classList.remove('wrong-input');
        }
    })

    $('#id_password1').on('blur', (e) => {
        let value = e.target.value;
        if(value.search(/^\d+$/) == -1 && value.length >= 8) {
            e.target.classList.remove('wrong-input');
            if(value == $('#id_password2').val()) {
                $('#id_password2').removeClass('wrong-input');
            }
        } else {
            e.target.classList.add('wrong-input');
        }
    })

    $('#id_password2').on('blur', (e) => {
        let value = e.target.value;
        if(value.search(/^\d+$/) == -1 && value.length >= 8 && value == $('#id_password1').val()) {
            e.target.classList.remove('wrong-input');
        } else {
            e.target.classList.add('wrong-input');
        }
    })

    $('.register-submit').on('click', (e) => {
        let validated = true;
        $('.wrong-input').removeClass('wrong-input');

        if(!/^[a-zA-Z0-9-_\.]+@[a-zA-Z0-9-_]+\.[a-zA-Z0-9-_]+$/.test($('#id_email').val())) {
            validated = false;
            $('#id_email').addClass('wrong-input');
        }
        if(!/^[0-9\+]+$/.test($('#id_phone_number').val())) {
            validated = false;
            $('#id_phone_number').addClass('wrong-input');
        }
        $('.med-input').each((i, input) => {
            if(!input.value && !input.classList.contains('register-fake-select')) {
                validated = false;
                input.classList.add('wrong-input');
            }
        })
        if(!$('.consultation-checkbox').is(":checked")) {
            validated = false;
            $('.consultation-checkbox-block > span').addClass('wrong-input');
        }

        if(!validated) {
            e.preventDefault();
        }
    })

})