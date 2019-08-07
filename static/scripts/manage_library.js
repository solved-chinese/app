$.post('/accounts/get_available_sets/', data => {
    data.sets.forEach(set => {
        $('#available-sets-container').append(`
            <div class="set-name-container" data-set-id="${set.pk}">
                <span>${ set.fields.name }</span>
                <i class="far fa-plus"></i>
            </div>
        `);
    });
});