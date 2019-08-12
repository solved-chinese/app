$(document).ready(function(){
    let is_fired = false;

    $('.choices').click(function(){
        if(is_fired)
            return;

        $.post(
            $(location).attr('href'),
            {user_answer: $(this).data('choice')},
            response => {
                $('#choice-div').append(
                    '<br><span>answer is '+response['correct_answer']+' you choose ' +
                    $(this).data('choice') + '</span>'
                );
                $('#next-button').show();
            }
        );
        is_fired = true;
    })
});