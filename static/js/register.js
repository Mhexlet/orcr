window.addEventListener('load', () => {

    let options = '';
    $('#id_field_of_activity > option').slice(1).each((i, option) => {
        options += `<span class="register-option" id="option-${option.value}">${option.innerHTML}</span>`
    })
    $('.register-options-block').append(options);
    // if(!$('#id_field_of_activity > option:selected').val()) {
    //     $('#id_field_of_activity > option:selected').removeAttr('selected');
    //     $('#id_field_of_activity > option:nth-child(2)').attr('selected', true);
    // }
    // $('.register-selected').html($('#id_field_of_activity > option:nth-child(2)').html());

    $('#id_birthdate').attr('type', 'date');
    $('#id_birthdate').attr('max', new Date().toISOString().split("T")[0]);

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

    $(document).on('input', '.note-editable', (e) => {
        $('#id_description').html(e.target.innerHTML);
    })

    $('#id_photo').on('change', (e) => {
        $('.edit-profile-photo-block').css('display', 'flex');
        $('.faq-background').css('display', 'flex');
        $('.register-photo-label').html(`Фото выбрано: ${e.target.files[0].name}`);
        let reader = new FileReader();

        reader.onload = function(e) {
            croppie.croppie('bind', {url: e.target.result});
        };

        reader.readAsDataURL(e.target.files[0]);
    })

    $('.edit-profile-photo-save').on('click', () => {
        croppie.croppie('result', {
            type: 'blob',
            format: 'jpeg',
        }).then(function (blob) {
            const file = new File([blob], "Photo.jpg", { type: "image/jpeg" });
            const dataTransfer = new DataTransfer();
            dataTransfer.items.add(file);
            document.getElementById('id_photo').files = dataTransfer.files;
        });
        $('.edit-profile-photo-block').css('display', '');
        $('.faq-background').css('display', '');
    })

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
        $('.register-fake-select').removeClass('wrong-input');
    })

    // $('.datepicker').datepicker({
    //     changeMonth: true,
    //     changeYear: true,
    //     yearRange: "c-100:c+0",
    //     dateFormat: "dd-mm-yy"
    // });

    // $('.datepicker').on('focus', () => {
    //     $('.datepicker').prop( "disabled", true );
    // })

    // $('.datepicker').on('blur', (e) => {
    //     $('.datepicker').prop( "disabled", false );
    // })

    $('.med-input').on('blur', (e) => {
        if(!['id_email', 'register-fake-select', 'id_birthdate'].includes(e.target.id)) {
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

    $('#id_phone_number').on('keydown', (e) => {
        let symbol = String.fromCharCode(e.keyCode);
        let regEx = /[0-9]/
        if (!regEx.test(symbol) && ![8, 9, 13, 27].includes(e.keyCode) && !(e.keyCode == 187 && e.shiftKey)) {
            e.preventDefault();
        }
    })

    $('#id_phone_number').on('input', (e) => {
        if(!/^[0-9\+]+$/.test(e.target.value)) {
            e.target.value = '';
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
            if(!input.value && !input.classList.contains('register-fake-select') && input.id) {
                console.log(input.id)
                validated = false;
                input.classList.add('wrong-input');
            }
        })
        if(!$('.consultation-checkbox').is(":checked")) {
            validated = false;
            $('.consultation-checkbox-block > span').addClass('wrong-input');
        }
        console.log($('.register-field-of-activity > option').filter('[selected=selected]').val())
        if(!$('.register-field-of-activity > option').filter('[selected=selected]').val()) {
            validated = false;
            $('.register-fake-select').addClass('wrong-input');
        }

        if(!validated) {
            e.preventDefault();
        }
    })

})