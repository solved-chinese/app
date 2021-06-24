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

$(document).on("click", ".tag-button", function () {
  let checkmark = $(this).find(".checkmark");
  if (checkmark.is(":hidden")) {
    // select
    $(".checkmark").hide();
    checkmark.show();
    selected_tags = [checkmark.data("pk")];
    $("#study-button").show();
  } else {
    // deselect
    checkmark.hide();
    selected_tags = [];
    $("#study-button").hide();
  }
});

$("#study-button").click(function () {
  // let activated = $('.slider-value.value-activated');
  // let minutes = parseInt($(activated[activated.length - 1]).attr('data-value'));
  // $('start-learning-form-minutes').val(minutes)
  $("#start-learning-form-filter").val(JSON.stringify(selected_tags));
  $("#start-learning-form").submit();
});
