let fontSize = getCookie('font-size');
let backgroundColor = getCookie('background-color');
let letterSpacing = getCookie('letter-spacing');
let imagesOff = getCookie('images');
let PVHidden = getCookie('hidden');

if(getCookie('poor-vision') == 'on') {
    $('head').append('<link rel="stylesheet" href="/static/css/poor-vision/poor-vision.css" id="pv-poor-vision">');

    if(fontSize != undefined && fontSize != 'off') {
        $('head').append(`<link rel="stylesheet" href="/static/css/poor-vision/font-${fontSize}.css" id="pv-font-size">`);
    }

    if(backgroundColor != undefined && backgroundColor != 'off') {
        $('head').append(`<link rel="stylesheet" href="/static/css/poor-vision/bg-${backgroundColor}.css" id="pv-background-color">`);
    }

    if(letterSpacing != undefined && letterSpacing != 'off') {
        $('head').append(`<link rel="stylesheet" href="/static/css/poor-vision/ls-${letterSpacing}.css" id="pv-letter-spacing">`);
    }

    if(imagesOff == 'off') {
        $('head').append('<link rel="stylesheet" href="/static/css/poor-vision/images-off.css" id="pv-images">');
    }

    if(PVHidden == 'on') {
        $('head').append('<link rel="stylesheet" href="/static/css/poor-vision/poor-vision-hidden.css" id="pv-poor-vision-hidden">');
    }
}

function getCookie(value) {
    let matches = document.cookie.match(new RegExp(
      "(?:^|; )" + value + "=([^;]*)"
    ));
    return matches ? decodeURIComponent(matches[1]) : undefined;
};

window.addEventListener('load', () => {

    if(imagesOff == 'off') {
        $('#images-off').html('Включить');
        $('#images-off').attr('id', 'images-on');
    }

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

    $('.header-menu-show').on('click', () => {
        $('.base-sidebar').animate({
            'left': 0
        }, 500)
        $('.base-background').css('display', 'block');
    })

    $('.base-background').on('click', () => {
        $('.base-sidebar').animate({
            'left': '-300px'
        }, 500)
        $('.base-background').css('display', '');
    })

    $('.header-poor-vision').on('click', () => {
        $('head').append('<link rel="stylesheet" href="/static/css/poor-vision/poor-vision.css" id="pv-poor-vision">');
        document.cookie = 'poor-vision=on; path=/';

        if(getCookie('font-size') != undefined && fontSize != 'off') {
            $('head').append(`<link rel="stylesheet" href="/static/css/poor-vision/font-${fontSize}.css" id="pv-font-size">`);
        }
    
        if(getCookie('background-color') != undefined && backgroundColor != 'off') {
            $('head').append(`<link rel="stylesheet" href="/static/css/poor-vision/bg-${backgroundColor}.css" id="pv-background-color">`);
        }
    
        if(getCookie('letter-spacing') != undefined && letterSpacing != 'off') {
            $('head').append(`<link rel="stylesheet" href="/static/css/poor-vision/ls-${letterSpacing}.css" id="pv-letter-spacing">`);
        }
    
        if(getCookie('images') == 'off') {
            $('head').append('<link rel="stylesheet" href="/static/css/poor-vision/images-off.css" id="pv-images">');
        }
    
        if(getCookie('hidden') == 'on') {
            $('head').append('<link rel="stylesheet" href="/static/css/poor-vision/poor-vision-hidden.css" id="pv-poor-vision-hidden">');
        }
    })

    $('.poor-vision-hide').on('click', (e) => {
        if($('#pv-poor-vision-hidden').length > 0) {
            document.cookie = 'hidden=off; path=/';
            $('#pv-poor-vision-hidden').remove();
        } else {
            document.cookie = 'hidden=on; path=/';
            $('head').append('<link rel="stylesheet" href="/static/css/poor-vision/poor-vision-hidden.css" id="pv-poor-vision-hidden">');
        }
    })

    $('.poor-vision-settings').on('click', (e) => {
        $('#pv-poor-vision-hidden').remove();
        document.cookie = 'hidden=off; path=/';
    })

    $('.poor-vision-normal').on('click', () => {
        document.cookie = 'poor-vision=off; path=/';
        $('#pv-poor-vision').remove();
        $('#pv-font-size').remove();
        $('#pv-background-color').remove();
        $('#pv-letter-spacing').remove();
        $('#pv-images').remove();
        $('#pv-poor-vision-hidden').remove();
    })

    $('.poor-vision-option').on('click', (e) => {
        let id = e.target.id;
        let type = id.replace(/-[a-z0-9]+/g, '');
        let value = id.replace(/[a-z]+-/g, '');
        let data = {
            'font': 'font-size',
            'bg': 'background-color',
            'ls': 'letter-spacing',
            'images': 'images'
        }
        document.cookie = `${data[type]}=${value}; path=/`;
        $(`#pv-${data[type]}`).remove();
        if(value != 'off') {
            $('head').append(`<link rel="stylesheet" href="/static/css/poor-vision/${id}.css" id="pv-${data[type]}">`);
        }
        
        if(type == 'images') {
            if(value == 'off') {
                $('#images-off').html('Включить');
                $('#images-off').attr('id', 'images-on');
                $('head').append(`<link rel="stylesheet" href="/static/css/poor-vision/images-off.css" id="pv-images">`);
            } else {
                $('#images-on').html('Отключить');
                $('#images-on').attr('id', 'images-off');
            }
        }
    })

    window.addEventListener('resize', () => {
        if(window.innerWidth >= 1024) {
            $('.base-sidebar').css('left', '');
            $('.base-background').css('display', '');
        } 
    })
})

