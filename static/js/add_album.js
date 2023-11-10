window.addEventListener('load', () => {

    $('.create-article-add-file').on('click', () => {
        let pk = $('.create-article-file-block').length;
        $('.create-article-files').append(`<div class="create-article-file-block">
                                                <input type="text" class="med-input create-article-file-name" placeholder="Подпись к файлу" id="name-${pk}">
                                                <input type="file" class="med-input create-article-file" id="file-${pk}">
                                                <div class="create-article-remove-file">+</div>
                                            </div>`);
    })

    $(document).on('click', '.create-article-remove-file', (e) => {
        if($('.create-article-file-block').length > 1) {
            e.target.parentNode.remove();
        } else {
            e.target.parentNode.innerHTML = `<input type="text" class="med-input create-article-file-name" placeholder="Подпись к файлу" id="name-0">
            <input type="file" class="med-input create-article-file" id="file-0">
            <div class="create-article-remove-file">+</div>`;
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

    $('#album-submit').on('click', () => {
        ajaxFunction('album');
    })

    $('#fileset-submit').on('click', () => {
        ajaxFunction('fileset');
    })

    function ajaxFunction(instance) {
        const token = $('input[name=csrfmiddlewaretoken]').val();
        let name = $('#custom-name').val();
        let page = $('.register-selected').attr('id').replace('selected-', '');
        let formData = new FormData();
        let files = [];
        $('.create-article-file').each((i, block) => {
            if(block.tagName == 'INPUT') {
                if(block.files.length) {
                    let pk = block.id.replace('file-', '');
                    formData.append(`${pk}-${$(`#name-${pk}`).val()}`, block.files[0]);
                }
            } else {
                files.push(block.id.replace('file-pk', ''));
            }
        })
        formData.append('csrfmiddlewaretoken', token);
        formData.append('name', name);
        formData.append('page', page);
        $.ajax({
            method: "post",
            url: `/custom/add_${instance}/`,
            contentType: false,
            processData: false,
            data: formData,
            success: (data) => {
                if(data['result'] == 'ok') {
                    $('.custom-content').html('<div class="custom-notification faq-form-notification" style="margin-top: 10px;">Альбом успешно добавлен</div>');
                } else if(data['result'] == 'failed') {
                    $('.custom-notification').html('Упс, что-то пошло не так. Попробуйте позже :с');
                    $('.custom-notification').css({'display': 'block', 'margin-top': '10px'});
                }
            },
            error: (data) => {
            }
        });
    }
})