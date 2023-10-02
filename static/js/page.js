window.addEventListener('load', () => {

    $('.faq-background').on('click', () => {
        $('.faq-background').css('display', '');
    })

    $('.page-album-img').on('click', (e) => {
        $('.page-background-img').attr('src', e.target.src);
        $('.faq-background').css('display', 'flex');
    })
})