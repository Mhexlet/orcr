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

    $('.create-article-submit').on('click', () => {
        ajaxFunction('create');
    })

    $('.edit-article-submit').on('click', () => {
        ajaxFunction('edit');
    })

    function ajaxFunction(action) {
        const token = $('input[name=csrfmiddlewaretoken]').val();
        let theme = $('.create-article-theme').val();
        let title = $('.create-article-title').val();
        let text = $('.create-article-text').val();
        let validated = true;

        $('.wrong-input').removeClass('wrong-input');

        if(!theme) {
            validated = false;
            $('.create-article-theme').addClass('wrong-input');
        } 

        if(!title) {
            validated = false;
            $('.create-article-title').addClass('wrong-input');
        } 

        if(!text) {
            validated = false;
            $('.create-article-text').addClass('wrong-input');
        }

        if(validated) {
            let formData = new FormData();
            let keptFiles = [];
            $('.create-article-file').each((i, block) => {
                if(block.tagName == 'INPUT') {
                    if(block.files.length) {
                        let pk = block.id.replace('file-', '');
                        formData.append(`${pk}-${$(`#name-${pk}`).val()}`, block.files[0]);
                    }
                } else {
                    keptFiles.push(block.id.replace('file-pk', ''));
                }
            })
            formData.append('csrfmiddlewaretoken', token);
            formData.append('g-recaptcha-response', $('#g-recaptcha-response').val());
            formData.append('theme', theme);
            formData.append('title', title);
            formData.append('text', text);
            if(action == 'edit') {
                formData.append('kept_files', keptFiles);
                let hrefParams = document.location.href.split('/');
                formData.append('pk', hrefParams[hrefParams.length - 2]);
            }
            $.ajax({
                method: "post",
                url: `/specialists/${action}_article/`,
                contentType: false,
                processData: false,
                data: formData,
                success: (data) => {
                    if(data['result'] == 'ok') {
                        $('.create-article-notification').css('display', '');
                        $('.faq-background').css('display', 'flex');
                    } else if(data['result'] == 'captcha') {
                        $('.create-article-notification').html('Капча не пройдена');
                        $('.create-article-notification').css('display', 'block');
                    } else if(data['result'] == 'failed') {
                        $('.create-article-notification').html('Упс, что-то пошло не так. Попробуйте позже :с');
                        $('.create-article-notification').css('display', 'block');
                    }
                },
                error: (data) => {
                }
            });
        }
    }

})