function getRadicalContainer(radical) {
    return `<div class="radical-container">
                <p>${ radical.pinyin }</p>
                <p class="radical-title">${ radical.chinese }</p>
                <p>${ radical.definition }</p>
                <div class="radical-pictograph" style="background-image: url(${ radical.mnemonic_image })"></div>
                <p>${ radical.mnemonic_explanation }</p>
            </div>`
}

function updateRadical() {
    let charRadicalsContainer = $(`.character-card-container[data-char-id=${selectedCharId}] .radicals-breakdown-container`);
    radicalIds = charRadicalsContainer
                 .attr('data-radical-ids')
                 .split(/\s/)
                 .filter(e => e != 0);
    charRadicalsContainer.empty();
    radicalIds.forEach(radicalId => {
        let radical = radicalsLookup[radicalId];
        if (!radical) {
            $.get(`/content/radical/${radicalId}`, radical => {
                radicalsLookup[radicalId] = radical;
                charRadicalsContainer.append(getRadicalContainer(radical));
            });
        } else {
            charRadicalsContainer.append(getRadicalContainer(radical));
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
    $.ajax({
        url: `/learning/student_character_tag/${setId}`,
        type: 'DELETE',
        success: function (result) {
            window.location.href = '/learning/manage_library/';
        }
    });
});
