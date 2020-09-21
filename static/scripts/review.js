let alreadyAnswered = false;

$('.option').on('click', e => {
    if (alreadyAnswered) return;

    let el = $(e.target);
    let chosen = el.data('choice');
    let correct;

    $.post('.', {user_answer: chosen}, response => {
        correct = response.correct_answer;
        if (correct !== chosen && chosen !== 4) {
            el.addClass('wrong');
        }
    })
    .done(() => {
        alreadyAnswered = true;
        $.each($('.option'), (i, btn) => {
            btn = $(btn);
            let answerId = btn.data('choice');
            if (answerId === correct) {
                btn.addClass('correct');
                 if (answerId === chosen) {
                    btn.addClass('chosen');
                 }
            } else if (answerId !== chosen || chosen === 4) {
                btn.addClass('disabled');
            }
        });
        $('#next-button').show();
    });
});
