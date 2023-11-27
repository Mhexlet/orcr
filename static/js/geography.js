window.addEventListener('load', () => {

    $('.geo-place:first-child').addClass('selected');
    $('.geo-name-block:nth-child(2)').addClass('selected');

    $('.geo-name-block').on('click', (e) => {
        if(e.target.classList.contains('geo-name-block') && !e.target.classList.contains('selected')) {
            $('.geo-place.selected').removeClass('selected');
            $(`#${e.target.id.replace('name', 'src')}`).addClass('selected');

            $('.geo-info-block').css('display', 'none');
            $(`#${e.target.id.replace('name', 'info')}`).css('display', 'block');
            $('.geo-name-block.selected').removeClass('selected');
            e.target.classList.add('selected');
        }
    })
})