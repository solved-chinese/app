function updateRadical() {
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
                radicalsLookup[radicalId] = radical;
                charRadicalsContainer.append(`
                <div class="radical-container">
                    <p>${ radical.pinyin }</p>
                    <p class="radical-title">${ radical.chinese }</p>
                    <p>${ radical.definition }</p>
                    <div class="radical-pictograph" style="background-image: url(/media/${ radical.mnemonic_image })"></div>
                    <p>${ radical.mnemonic_explanation }</p>
                </div>`);
            });
        }
    });
}


const radicalsLookup = {};
let selectedChar = $($('.chars-container').children()[0]);
let selectedCharId = selectedChar.attr('data-char-id');

selectedChar.addClass('selected');
$(`.character-card-container[data-char-id=${selectedCharId}]`).parent().show();

updateRadical();


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

    updateRadical();
})

$('.delete-set-button').click(e => {
    let target = $(e.target);
    let setId = target.data('set-id');
    $.post('/accounts/delete_set/', {set_id: setId}, data => {
        if (data.msg === 'good') {
            window.location.href = '/accounts/manage_library/';
        }
    });
});
