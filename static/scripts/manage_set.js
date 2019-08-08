function displayRadicals(charId) {
    $(`#character-card-container[data-char-id=${charId}]`).parent().show();
}

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
})