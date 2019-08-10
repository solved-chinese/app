function pad(num, size) {
    let s = num + '';
    while (s.length < size) s = '0' + s;
    return s;
}


const radicalsLookup = {};
let selectedChar = $($('.chars-container').children()[0]);
let selectedCharId = selectedChar.attr('data-char-id');


selectedChar.addClass('selected');
$(`.character-card-container[data-char-id=${selectedCharId}]`).parent().show();

$('.char').click(e => {
    let el = $(e.target);
    while (!el.attr('class').split(/\s+/).includes('char')) el = el.parent();
    let chosenCharId = el.attr('data-char-id');
    if (chosenCharId === selectedCharId) return;

    selectedChar.removeClass('selected');
    $(`.character-card-container[data-char-id=${selectedCharId}]`).parent().hide();

    selectedChar = el;
    selectedCharId = chosenCharId;
    selectedChar.addClass('selected');
    $(`.character-card-container[data-char-id=${selectedCharId}]`).parent().show();

    // Show radicals info
    let charRadicalsContainer = $(`.character-card-container[data-char-id=${selectedCharId}] .radicals-breakdown-container`);
    radicalIds = charRadicalsContainer
                 .attr('data-radical-ids')
                 .split(/\s/)
                 .filter(e => e != 0);
    charRadicalsContainer.empty();
    radicalIds.forEach(radicalId => {
        let radical = radicalsLookup[radicalId];
        if (radical) {
            charRadicalsContainer.append(`
            <div class="radical-container">
                <p>${ radical.pinyin }</p>
                <p class="radical-title">${ radical.chinese }</p>
                <p>${ radical.definition }</p>
                <div class="radical-pictograph" style="background-image: url(/media/${ radical.mnemonic_image })"></div>
                <p>${ radical.mnemonic_explanation }</p>
            </div>`);
        } else {
            $.post('/learning/get_radical/', {radical_id: radicalId}, data => {
                radical = data.radical.fields;
                console.log(radical);
                radicalsLookup[radicalId] = radical;
                charRadicalsContainer.append(`
                <div class="radical-container">
                    <p>${ radical.pinyin }</p>
                    <p class="radical-title">${ radical.chinese }</p>
                    <p>${ radical.definition }</p>
                    <div class="radical-pictograph" style="background-image: url(/media/${ radical.mnemonic_image })"></div>
                    <p>${ radical.mnemonic_explanation }</p>
                </div>`);
            })
        }
        console.log(radical);
    });
})
