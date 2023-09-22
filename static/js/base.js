window.addEventListener('load', () => {

    $('.menu-section-block').on('click', (e) => {
        let id = e.target.id.replace('menu-section-', '');
        let dropdown = $(`#menu-dropdown-${id}`);
        if(dropdown.css('display') == 'flex') {
            dropdown.animate({
                'height': 0
            }, 400, () => {
                dropdown.css('display', '');
                e.target.classList.remove('active');
            });
            $(`#menu-section-${id} > .menu-section-arrow`).css('transform', 'rotate(90deg)');
        } else {
            dropdown.css({'overflow': 'hidden', 'display': 'flex'});
            let height = 0;
            $(`#menu-dropdown-${id} > .menu-section-page`).each((i, item) => {
                height += item.clientHeight;
            })
            dropdown.animate({
                'height': height
            }, 300, () => {
                dropdown.css('overflow', '');
                e.target.classList.add('active');
            })
            $(`#menu-section-${id} > .menu-section-arrow`).css('transform', 'rotate(-90deg)');
        }
    })

})

