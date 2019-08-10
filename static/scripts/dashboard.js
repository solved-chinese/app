let snapPoints; // stores the x-coordinates of the slider values


function checkForm () {
    let form = $("#form");
    let is_legal = false;
    
    for (let index = 2; index < form.elements.length-1; index+=2) {
        if (form.elements[index].value !== form.elements[index+1].value) {
            is_legal = true;
        }
    }

    let pattern = /^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})$/;
    if (!pattern.test($("input[name|='email']")[0].value)) {
        is_legal = false;
        alert("Illegal email address.");
    }

    pattern = /^(?!_)(?!.*?_$)[a-zA-Z0-9_\u4e00-\u9fa5]+$/;
    if (!pattern.test($("input[name|='first_name']")[0].value) || !pattern.test($("input[name|='last_name']")[0].value)) {
        if ($("input[name|='first_name']")[0].value !== "" && $("input[name|='last_name']")[0].value !== "") {
            is_legal = false;
            alert("Illegal names");
        }
    }

    if (is_legal) {
        form.submit();
        $("#success-alert").css("visibility", "visible");
    }

}

function updateSlider(e) {
    // !!!!!!!!!!!!!!
    // This is a very stupid implementation of the slider
    // Definitely needs further optimization and adjustments
    // !!!!!!!!!!!!!!

    // Find the closets slider value to the click
    let diffs = snapPoints.map(x => Math.abs(x - e.pageX));
    let closestIndex = diffs.indexOf(Math.min(...diffs));

    // Toggle slider values accordingly
    $('.slider-value').toArray().forEach((el, i, arr) => {
        if (i <= closestIndex) {
            $(el).addClass('value-activated');
        } else {
            $(el).removeClass('value-activated');
        }
    })

    // Change activate bar width
    let activePercent = $('.slider-value')[closestIndex].getAttribute('data-width-percent') + '%';
    $('#slider-activated').css('width', activePercent);

    // Update slider value text
    let activeValue = $('.slider-value')[closestIndex].getAttribute('data-value');
    $('#slider-value-text').html(activeValue + '&#8239;min');
    let labelWidth = $('#slider-value-text').width() + 'px';
    $('#slider-value-text').css('margin-left', `calc(${activePercent} - ${labelWidth} / 2)`);
}

$('#slider-bar').mousedown(e => {
    // Get the x-coordinates of all slider values
    snapPoints = [];
    $('.slider-value').each((i, el) => snapPoints.push($(el).offset().left + $(el).width() / 2));
    updateSlider(e);
    $(this).mousemove(e => updateSlider(e));
})
.mouseup(() => $(this).off('mousemove'));

// Initial position offset
let labelWidth = $('#slider-value-text').width() + 'px';
$('#slider-value-text').css('margin-left', `calc(-${labelWidth} / 2)`);


$('#study-button').click(e => {
    let activated = $('.slider-value.value-activated');
    let minutes = parseInt($(activated[activated.length - 1]).attr('data-value'));
    $.post('/learning/start_learning/', {minutes_to_learn: minutes}, data => {
        // console.log(data);
        // console.log(data.responseText);
        // $('html').html(data.responseText);
    });
})