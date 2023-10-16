window.addEventListener('load', () => {

    let textData = {};
    
    function getCssStyle(el, prop) {
        return window.getComputedStyle(el, null).getPropertyValue(prop);
    }

    function getCanvasFont(el) {
        const fontWeight = getCssStyle(el, 'font-weight') || 'normal';
        const fontSize = getCssStyle(el, 'font-size') || '16px';
        const fontFamily = getCssStyle(el, 'font-family') || 'Times New Roman';

        return `${fontWeight} ${fontSize} ${fontFamily.split(',')[0]}`;
    }

    function getTextWidth(text, font, letterSpacing) {
        const canvas = getTextWidth.canvas || (getTextWidth.canvas = document.createElement("canvas"));
        const context = canvas.getContext("2d");
        context.font = font;
        context.letterSpacing = letterSpacing;
        const metrics = context.measureText(text);
        return metrics.width;
    }

    function adjustText(block, text, maxLines) {
        let words = text.split(' ');
        let blockWidth = block.clientWidth;
        let currentLineLength = 0;
        let currentLineNumber = 1;
        let result = '';
        let font = getCanvasFont(block);
        let letterSpacing = getCssStyle(block, 'letter-spacing');
        let readMoreLength = getTextWidth('...', font, letterSpacing);
        for(let word of words) {
            word += ' ';
            let wordLength = getTextWidth(word, font, letterSpacing);
            if(wordLength <= blockWidth - currentLineLength) {
                currentLineLength += wordLength;
                result += word;
            } else {
                if(currentLineNumber != maxLines) {
                    currentLineNumber++;
                    currentLineLength = 0;
                }
                if(currentLineNumber == maxLines) {
                    blockWidth -= readMoreLength;
                }
                if(currentLineNumber == maxLines && wordLength > blockWidth - currentLineLength) {
                    let charactersCount = Math.floor((blockWidth - currentLineLength) / wordLength * word.length);
                    result += word.slice(0, charactersCount >= 0 ? charactersCount : 0) + '...';
                    currentLineLength = blockWidth;
                    break;
                } else {
                    currentLineLength += wordLength;
                    result += word;
                }
            }
        }
        block.innerHTML = result;
    }
    
    function adjustEventsTexts() {
    	$('.text-to-adjust').each((i, text) => {
            adjustText(text, textData[text.id], 2);
        })
    }
    
    $('.text-to-adjust').each((i, text) => {
        textData[text.id] = text.innerText;
    });
    adjustEventsTexts();

    $('.faq-faq-block').on('click', (e) => {
        let question = e.target.children[2];
        let answer = e.target.children[3];
        if(question.classList.contains('text-to-adjust')) {
            question.classList.remove('text-to-adjust');
            question.classList.add('text-not-to-adjust');
            question.innerHTML = textData[question.id];

            answer.classList.remove('text-to-adjust');
            answer.classList.add('text-not-to-adjust');
            answer.innerHTML = textData[answer.id];
        } else {
            question.classList.add('text-to-adjust');
            question.classList.remove('text-not-to-adjust');
            adjustText(question, textData[question.id], 2);

            answer.classList.add('text-to-adjust');
            answer.classList.remove('text-not-to-adjust');
            adjustText(answer, textData[answer.id], 2);
        }
    })

    $('.reviews-subblock').on('click', (e) => {
        let review = e.target.children[1].children[1];
        if(review.classList.contains('text-to-adjust')) {
            review.classList.remove('text-to-adjust');
            review.classList.add('text-not-to-adjust');
            review.innerHTML = textData[review.id];
        } else {
            review.classList.add('text-to-adjust');
            review.classList.remove('text-not-to-adjust');
            adjustText(review, textData[review.id], 2);
        }
    })
    
    window.addEventListener('resize', () => {
        adjustEventsTexts();
    })
})