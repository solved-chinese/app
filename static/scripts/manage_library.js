$.post('/accounts/get_available_sets/', data => {
    data.sets.forEach(set => {
        $('#available-sets-container').append(`
            <div class="set-name-container" data-set-id="${ set.pk }">
                <span>${ set.fields.name }</span>
                <i class="far fa-plus list-add-set-button"></i>
            </div>
        `);
    });
    $('.list-add-set-button').off('click').click(e => {
        let target = $(e.target)
        let parent = target.parent();
        let parentId = parent.attr('data-set-id');
        let setName = parent.find('span').html();
        $.post('/accounts/add_set/', {set_id: parentId}, data => {
            if (data.msg === 'good') {
                parent.remove();
                $('#char-sets-container #add-set-button-container').before(`
                    <div class="char-set" data-set-pk="${ parentId }">
                        <img class="char-set-cover" src="/static/images/set-covers/default-set-cover.jpg">
                        <p class="char-set-title">${ setName }</p>
                    </div>
                `);
                $('.char-set').off('click').click(charSetClick);
            }
        });
    });
});

function charSetClick(e) {
    let el = $(e.target);
    while (el.attr('class') !== 'char-set') el = el.parent();
    if (el.attr('id') === 'add-set-button-container') return;
    let pk = el.attr('data-set-pk');
    window.location.href += pk;
}

$('.char-set').click(charSetClick);

$('#add-set-button-container').click(e => {
    showModal('add-new-set-modal');
});

$('.modal-close-button').click(e => {
    hideModal(e.target.parentElement.parentElement.id);
});
