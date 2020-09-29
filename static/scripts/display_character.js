const pk = $('meta[name=pk]').attr('content');
let audio;

$.get({
    url: '/learning/getAudio/',
    data: {
        t: $('#character-text').text(),
        pk: pk
    }
})
.done(data => {
    if (data.success) {
        audio = new Howl({
            src: [`/media/audio/${pk}.mp3`]
        });
        audio.play();
        $('#speak-button').removeClass('disabled');
        $('#speak-button').click(() => audio.play());
    }
})
.fail((jqXhr, textStatus, errorMessage) => {
    $('#audio-error-msg').fadeIn();
    setTimeout(() => {
        $('#audio-error-msg').fadeOut();
    }, 3500);
});
