window.addEventListener('load', () => {

    const imagesCount = slides.length - 1;
    let currentImage = 0;
    let currentTimer;
    let locked = false;

    function getHtmlString(position) {
        let htmlString = `<div class="index-slide-block index-${position}-slide"><img src="/media/${slides[currentImage].fields.image}" alt="image"></div>`;
        if(slides[currentImage].fields.link) {
            htmlString = `<a href="${slides[currentImage].fields.link}" class="index-slide-block index-${position}-slide"><img src="/media/${slides[currentImage].fields.image}" alt="image"></a>`;
        }
        return htmlString;
    }

    $('.index-slides-block').append(getHtmlString('current'));
    
    currentTimer = setTimeout(timeoutChangeCurrent, 5000);

    $('.index-slider-left-arrow').animate({
        'left': '4%'
    }, 1000);

    $('.index-slider-right-arrow').animate({
        'right': '4%'
    }, 1000);

    function changeCurrent(direction=true) {
        let nextPosition = '100%';
        let currentPosition = 0;
        let prevPosition = '-100%';
        locked = true;
        if(direction) {
            $('.index-slides-block').prepend(getHtmlString('next'));
            $('.index-current-slide').animate({
                'left': prevPosition
            }, 600);
            $('.index-next-slide').animate({
                'left': currentPosition
            }, 600, () => {
                $('.index-current-slide').remove();
                $('.index-next-slide').addClass('index-current-slide');
                $('.index-current-slide').removeClass('index-next-slide');
                locked = false;
            });
        } else {
            $('.index-slides-block').prepend(getHtmlString('previous'));
            $('.index-current-slide').animate({
                'left': nextPosition
            }, 600);
            $('.index-previous-slide').animate({
                'left': currentPosition
            }, 600, () => {
                $('.index-current-slide').remove();
                $('.index-previous-slide').addClass('index-current-slide');
                $('.index-current-slide').removeClass('index-previous-slide');
                locked = false;
            });
        }
        clearTimeout(currentTimer);
        currentTimer = setTimeout(timeoutChangeCurrent, 5000);
    };

    function timeoutChangeCurrent() {
        if(currentImage == imagesCount) {
            currentImage = 0;
        } else {
            currentImage++;
        }
        changeCurrent();
    };

    $(document).on('click', '.index-slider-left-arrow', () => {
        if(!locked) {
            if(currentImage == 0) {
                currentImage = imagesCount;
            } else {
                currentImage--;
            }
            changeCurrent(false);
        };
    });

    $(document).on('click', '.index-slider-right-arrow', () => {
        if(!locked) {
            if(currentImage == imagesCount) {
                currentImage = 0;
            } else {
                currentImage++;
            }
            changeCurrent();
        };
    });

    $(document).on('keydown', (event) => {
        console.log(currentImage)
        let type = event.code;
        if(type == 'ArrowLeft') {
            $('.index-slider-left-arrow').click();
        } else if(type == 'ArrowRight') {
            $('.index-slider-right-arrow').click();
        }
    });

})