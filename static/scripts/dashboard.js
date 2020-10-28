// let snapPoints; // stores the x-coordinates of the slider values
//
//
// function updateSlider(e) {
//     // !!!!!!!!!!!!!!
//     // This is a very stupid implementation of the slider
//     // Definitely needs further optimization and adjustments
//     // !!!!!!!!!!!!!!
//
//     // Find the closets slider value to the click
//     let diffs = snapPoints.map(x => Math.abs(x - e.pageX));
//     let closestIndex = diffs.indexOf(Math.min(...diffs));
//
//     // Toggle slider values accordingly
//     $('.slider-value').toArray().forEach((el, i, arr) => {
//         if (i <= closestIndex) {
//             $(el).addClass('value-activated');
//         } else {
//             $(el).removeClass('value-activated');
//         }
//     })
//
//     // Change activate bar width
//     let activePercent = $('.slider-value')[closestIndex].getAttribute('data-width-percent') + '%';
//     $('#slider-activated').css('width', activePercent);
//
//     // Update slider value text
//     let activeValue = $('.slider-value')[closestIndex].getAttribute('data-value');
//     $('#slider-value-text').html(activeValue + '&#8239;min');
//     let labelWidth = $('#slider-value-text').width() + 'px';
//     $('#slider-value-text').css('margin-left', `calc(${activePercent} - ${labelWidth} / 2)`);
// }
//
// $('#slider-bar').mousedown(e => {
//     // Get the x-coordinates of all slider values
//     snapPoints = [];
//     $('.slider-value').each((i, el) => snapPoints.push($(el).offset().left + $(el).width() / 2));
//     updateSlider(e);
//     $(this).mousemove(e => updateSlider(e));
// })
// .mouseup(() => $(this).off('mousemove'));
//
// // Initial position offset
// let labelWidth = $('#slider-value-text').width() + 'px';
// $('#slider-value-text').css('margin-left', `calc(-${labelWidth} / 2)`);

var selected_tags = [];

// TODO this can totally be done without js
$.get('/learning/student_character_tag/', data => {
    if(data.length == 0) {
        $('#available-tags-container').append(`
            Please add at least one set to your library. You can do so in 
            "Manage Vocab Sets" on the top left corner.
        `);
    }
    data.forEach(tag => {
        states = ""
        Object.entries(tag.states_count).forEach(function([key, value]) {
           states += `${key}: ${value} &nbsp;&nbsp;&nbsp;`
        });
        $('#available-tags-container').append(`
            <button type="button" class="button button-secondary tag-button text-left">
                <div class='tag-name'>
                  ${tag.name} 
                  <span class="checkmark" data-pk="${tag.pk}">&#10003;</span> 
                </div>
                ${states}
            </button>
        `);
    });

    $(document).on("click", ".tag-button" , function() {
        let checkmark = $(this).find('.checkmark');
        checkmark.toggle();
        let pk = checkmark.data("pk");
        if(checkmark.is(":hidden")) {
            selected_tags.splice(selected_tags.indexOf(pk), 1);
        } else {
            selected_tags.push(pk);
        }
        console.log(selected_tags);
        if (selected_tags.length == 0) {
            $("#study-button").hide();
        } else {
            $("#study-button").show();
        }
    });
});

$('#study-button').click(function() {
    // let activated = $('.slider-value.value-activated');
    // let minutes = parseInt($(activated[activated.length - 1]).attr('data-value'));
    // $('start-learning-form-minutes').val(minutes)
    $('#start-learning-form-filter').val(JSON.stringify(selected_tags));
    $('#start-learning-form').submit();
})
