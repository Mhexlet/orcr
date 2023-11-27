window.addEventListener('load', () => {

    const imagesCount = slides.length - 1;
    let currentImage = 0;
    let currentSliderTimer;
    let sliderLock = false;

    const bannersCount = banners.length - 1;
    let currentBanner = 0;
    let currentBannerTimer;
    let bannersLock = false;
    let bannersPerBlock = 3;
    if(window.innerWidth <= 620) {
        bannersPerBlock = 1;
    } else if(window.innerWidth <= 1300) {
        bannersPerBlock = 2;
    }

    const linksCount = links.length - 1;
    let currentLink = 0;
    let currentLinkTimer;
    let linksLock = false;

    console.log(links)

    function getHtmlString(position) {
        let htmlString = `<div class="index-slide-block index-${position}-slide"><img src="${slides[currentImage].image}" alt="image"></div>`;
        if(slides[currentImage].link) {
            htmlString = `<a href="${slides[currentImage].link}" class="index-slide-block index-${position}-slide" target="_blank"><img src="${slides[currentImage].image}" alt="image"></a>`;
        }
        return htmlString;
    }

    function getBannerBlock(position) {
        let htmlString = `<div class="index-banners-subblock index-${position}-banner">`;
        for(let i = 0; i < bannersPerBlock; i++) {
            if(bannersCount >= currentBanner + i) {
                htmlString += `<a href="${banners[currentBanner + i].link}" class="index-banner" target="_blank">
                                        <div class="index-banner-img-block"><img src="${banners[currentBanner + i].image}" alt="image"></div>
                                        <span class="index-answer">${banners[currentBanner + i].name}</span>
                                    </a>`;
            }
        }
        htmlString += '</div>';
        return htmlString;
    }

    function getLinkBlock(position) {
        let htmlString = `<div class="index-banners-subblock index-${position}-link">`;
        for(let i = 0; i < bannersPerBlock; i++) {
            if(linksCount >= currentLink + i) {
                htmlString += `<a href="${links[currentLink + i].link}" class="index-banner" target="_blank">
                                        <div class="index-banner-img-block"><img src="${links[currentLink + i].image}" alt="image"></div>
                                        <span class="index-answer">${links[currentLink + i].name}</span>
                                    </a>`;
            }
        }
        htmlString += '</div>';
        return htmlString;
    }

    $('.index-slides-block').append(getHtmlString('current'));
    $('.index-banners').append(getBannerBlock('current'));
    $('.index-links').append(getLinkBlock('current'));
    
    currentSliderTimer = setTimeout(timeoutChangeCurrentSlide, 10000);
    currentBannerTimer = setTimeout(timeoutChangeCurrentBanner, 10000);
    // currentLinkTimer = setTimeout(timeoutChangeCurrentLink, 10000);

    let position = window.innerWidth <= 540 ? '-10px' : '20px';
    $('.index-slider-left-arrow').animate({
        'left': position
    }, 1000);

    $('.index-slider-right-arrow').animate({
        'right': position
    }, 1000);

    function changeCurrentSlide(direction=true) {
        let nextPosition = '100%';
        let currentPosition = 0;
        let prevPosition = '-100%';
        sliderLock = true;
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
                sliderLock = false;
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
                sliderLock = false;
            });
        }
        clearTimeout(currentSliderTimer);
        currentSliderTimer = setTimeout(timeoutChangeCurrentSlide, 10000);
    };

    function changeCurrentBanner(direction=true) {
        let nextPosition = '100%';
        let currentPosition = 0;
        let prevPosition = '-100%';
        bannersLock = true;
        if(direction) {
            $('.index-banners').prepend(getBannerBlock('next'));
            $('.index-current-banner').animate({
                'left': prevPosition
            }, 600);
            $('.index-next-banner').animate({
                'left': currentPosition
            }, 600, () => {
                $('.index-current-banner').remove();
                $('.index-next-banner').addClass('index-current-banner');
                $('.index-current-banner').removeClass('index-next-banner');
                bannersLock = false;
            });
        } else {
            $('.index-banners').prepend(getBannerBlock('previous'));
            $('.index-current-banner').animate({
                'left': nextPosition
            }, 600);
            $('.index-previous-banner').animate({
                'left': currentPosition
            }, 600, () => {
                $('.index-current-banner').remove();
                $('.index-previous-banner').addClass('index-current-banner');
                $('.index-current-banner').removeClass('index-previous-banner');
                bannersLock = false;
            });
        }
        clearTimeout(currentBannerTimer);
        currentBannerTimer = setTimeout(timeoutChangeCurrentBanner, 10000);
    };

    function changeCurrentLink(direction=true) {
        let nextPosition = '100%';
        let currentPosition = 0;
        let prevPosition = '-100%';
        linksLock = true;
        if(direction) {
            $('.index-links').prepend(getLinkBlock('next'));
            $('.index-current-link').animate({
                'left': prevPosition
            }, 600);
            $('.index-next-link').animate({
                'left': currentPosition
            }, 600, () => {
                $('.index-current-link').remove();
                $('.index-next-link').addClass('index-current-link');
                $('.index-current-link').removeClass('index-next-link');
                linksLock = false;
            });
        } else {
            $('.index-links').prepend(getLinkBlock('previous'));
            $('.index-current-link').animate({
                'left': nextPosition
            }, 600);
            $('.index-previous-link').animate({
                'left': currentPosition
            }, 600, () => {
                $('.index-current-link').remove();
                $('.index-previous-link').addClass('index-current-link');
                $('.index-current-link').removeClass('index-previous-link');
                linksLock = false;
            });
        }
        clearTimeout(currentLinkTimer);
        currentLinkTimer = setTimeout(timeoutChangeCurrentLink, 10000);
    };

    function timeoutChangeCurrentSlide() {
        if(currentImage == imagesCount) {
            currentImage = 0;
        } else {
            currentImage++;
        }
        changeCurrentSlide();
    };

    function timeoutChangeCurrentBanner() {
        if(currentBanner + bannersPerBlock >= bannersCount) {
            currentBanner = 0;
        } else {
            currentBanner += bannersPerBlock;
        }
        changeCurrentBanner();
    };

    function timeoutChangeCurrentLink() {
        if(currentLink + bannersPerBlock >= linksCount) {
            currentLink = 0;
        } else {
            currentLink += bannersPerBlock;
        }
        changeCurrentLink();
    };

    $(document).on('click', '.index-slider-left-arrow', () => {
        if(!sliderLock) {
            if(currentImage == 0) {
                currentImage = imagesCount;
            } else {
                currentImage--;
            }
            changeCurrentSlide(false);
        };
    });

    $(document).on('click', '.index-slider-right-arrow', () => {
        if(!sliderLock) {
            if(currentImage == imagesCount) {
                currentImage = 0;
            } else {
                currentImage++;
            }
            changeCurrentSlide();
        };
    });

    $(document).on('click', '.index-banner-left-arrow', () => {
        if(!bannersLock) {
            if(currentBanner == 0) {
                currentBanner = bannersCount - bannersCount % bannersPerBlock;
            } else {
                currentBanner -= bannersPerBlock;
            }
            changeCurrentBanner(false);
        };
    });

    $(document).on('click', '.index-banner-right-arrow', () => {
        if(!bannersLock) {
            if(currentBanner + bannersPerBlock >= bannersCount) {
                currentBanner = 0;
            } else {
                currentBanner += bannersPerBlock;
            }
            changeCurrentBanner();
        };
    });

    $(document).on('click', '.index-link-left-arrow', () => {
        if(!linksLock) {
            if(currentLink == 0) {
                currentLink = linksCount - linksCount % bannersPerBlock;
            } else {
                currentLink -= bannersPerBlock;
            }
            changeCurrentLink(false);
        };
    });

    $(document).on('click', '.index-link-right-arrow', () => {
        if(!linksLock) {
            if(currentLink + bannersPerBlock >= linksCount) {
                currentLink = 0;
            } else {
                currentLink += bannersPerBlock;
            }
            changeCurrentLink();
        };
    });

    $(document).on('keydown', (event) => {
        let type = event.code;
        if(type == 'ArrowLeft') {
            $('.index-slider-left-arrow').click();
        } else if(type == 'ArrowRight') {
            $('.index-slider-right-arrow').click();
        }
    });

    window.addEventListener('resize', () => {
        if(window.innerWidth <= 620) {
            bannersPerBlock = 1;
        } else if(window.innerWidth <= 1300) {
            bannersPerBlock = 2;
        } else {
            bannersPerBlock = 3;
        }
    })

})