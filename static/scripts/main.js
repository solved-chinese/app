/***********************************
  Modal Helper Functions
***********************************/

function showModal(modalId) {
    $('.page-mask').show();
    $(`#${modalId}`).show();
}

function hideModal(modalId) {
    $('.page-mask').hide();
    $(`#${modalId}`).hide();
}


/***********************************
  Search
***********************************/

const MAX_ENTRIES_DISPLAY = 6;
const $source = $('.search-input-wrapper > input');
const $target = $('#search-dropdown-wrapper');

$('.search-form-wrapper').focusout(() => {
    $target.html('');
});

function searchHandler(e) {
    let query = $source.val();
    if (query === '') {
        $target.html('');
        return;
    }

    $.post({
        url: '/learning/search/',
        data: {
            keyword: query
        }
    })
    .done(data => {
        $target.empty();
        $('<hr>').appendTo($target);

        if (data.characters.length === 0) {
            $('<div class="error-msg">No Match</div>').appendTo($target);
            return;
        }

        for (let char of data.characters.splice(0, MAX_ENTRIES_DISPLAY)) {
            let targetPk = char.pk.toString().padStart(4, '0');
            char = char.fields;
            let entry = `
                <a href='/learning/C${targetPk}' class='search-entry-wrapper'>
                    <div class='search-entry'>
                        <span class='character'>${char.chinese}</span>
                        <span class='pinyin'>${char.pinyin.replace(/\s+/g, '')}</span>
                        <p class='definition'>${char.definition_1}
                            <br />
                            <span class='explanation'>${char.explanation_2 || ''}</span>
                        </p>
                    </div>
                </a>`;
            // Some pinyins contain whitespaces, hence they are removed here (temporary fix)
            $(entry).appendTo($target);
        }
    })
    .fail((xhr, status, errorThrown) => {
        $target.html('<hr><div class="error-msg">There was a problem connecting with the Solved server</div>');
        return;
    });
}

// $(document).keypress(function(event){
//     if (event.keyCode == 13){ 
//         searchHandler(null, true);
//     }
// });

$source.on('input propertychange', searchHandler);
$source.keypress(e => {
    if (e.keyCode !== 13 || $('.search-entry-wrapper').length === 0) return;
    $('.search-entry-wrapper')[0].click();
});