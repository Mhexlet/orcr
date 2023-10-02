window.addEventListener('load', () => {

    $('.geo-place:first-child').addClass('selected');
    $('.geo-name:nth-child(2)').addClass('selected');

    $('.geo-name').on('click', (e) => {
        $('.geo-place.selected').removeClass('selected');
        $(`#${e.target.id.replace('name', 'src')}`).addClass('selected');

        $('.geo-name.selected').removeClass('selected');
        e.target.classList.add('selected');
    })
})