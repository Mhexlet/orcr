window.addEventListener('load', () => {

    $('.geo-place:first-child').addClass('selected');
    $('.geo-name-block:nth-child(2)').addClass('selected');

    $('.geo-name-block').on('click', (e) => {
        $('.geo-place.selected').removeClass('selected');
        $(`#${e.target.id.replace('name', 'src')}`).addClass('selected');

        $('.geo-name-block.selected').removeClass('selected');
        e.target.classList.add('selected');
    })
})