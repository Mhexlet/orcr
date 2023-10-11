window.addEventListener('load', () => {

    $('.account-delete-application').on('click', (e) => {
        $('.account-delete-confirm').attr('id', e.target.id.replace('delete-', 'confirm-'));
        $('.faq-background').css('display', 'flex');
    })

    $('.account-delete-article').on('click', (e) => {
        $('.account-delete-confirm').attr('id', e.target.id.replace('delete-article-', 'confirm-article-'));
        $('.faq-background').css('display', 'flex');
    })

    $('.account-delete-confirm').on('click', (e) => {
        const token = $('input[name=csrfmiddlewaretoken]').val();
        if(e.target.id.startsWith('confirm-article-')) {
            let pk = e.target.id.replace('confirm-article-', '');
            $.ajax({
                method: "post",
                url: "/specialists/delete_article/",
                data: {csrfmiddlewaretoken: token, pk: pk},
                success: (data) => {
                    if($(`#article-${pk}`).parent().children().length == 1) {
                        $(`#article-${pk}`).parent().append('<div class="account-block-none">Нет материалов в этой категории</div>');
                    }
                    $(`#article-${pk}`).remove();
                    $('.account-delete-confirm').removeAttr('id');
                    $('.faq-background').css('display', '');
                },
                error: (data) => {
                }
            });
        } else {
            let pk = e.target.id.replace('confirm-', '');
            $.ajax({
                method: "post",
                url: "/specialists/delete_application/",
                data: {csrfmiddlewaretoken: token, pk: pk},
                success: (data) => {
                    if($(`#application-${pk}`).parent().children().length == 1) {
                        $(`#application-${pk}`).parent().append('<div class="account-block-none">Нет материалов в этой категории</div>');
                    }
                    $(`#application-${pk}`).remove();
                    $('.account-delete-confirm').removeAttr('id');
                    $('.faq-background').css('display', '');
                },
                error: (data) => {
                }
            });
        }
    })

    $('.account-delete-cancel').on('click', () => {
        $('.account-delete-confirm').removeAttr('id');
        $('.faq-background').css('display', '');
    })

    $('.account-hide-article').on('click', (e) => {
        const token = $('input[name=csrfmiddlewaretoken]').val();
        let pk = e.target.id.replace('hide-', '');
        $.ajax({
            method: "post",
            url: "/specialists/hide_article/",
            data: {csrfmiddlewaretoken: token, pk: pk},
            success: (data) => {
                if($(`#article-${pk} > .account-article-content`).hasClass('account-hidden')) {
                    $(`#article-${pk} > .account-article-content`).removeClass('account-hidden');
                    e.target.innerHTML = 'Скрыть статью';
                } else {
                    $(`#article-${pk} > .account-article-content`).addClass('account-hidden');
                    e.target.innerHTML = 'Сделать видимой';
                }
            },
            error: (data) => {
            }
        });
    })
})