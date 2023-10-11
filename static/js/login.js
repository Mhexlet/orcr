window.addEventListener('load', () => {

    $('.med-input').on('blur', (e) => {
        if(!e.target.value) {
            e.target.classList.add('wrong-input');
        } else {
            e.target.classList.remove('wrong-input');
        }
    })

    $('.login-submit').on('click', (e) => {
        let validated = true;

        $('.med-input').each((i, input) => {
            if(!input.value) {
                validated = false;
                input.classList.add('wrong-input');
            }
        })

        if(!validated) {
            e.preventDefault();
        }
    })

})