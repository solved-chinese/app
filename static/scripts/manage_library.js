function get_available_sets() {
    $.post('/accounts/get_available_sets/', data => {
        console.log(data.sets)
    });
}
