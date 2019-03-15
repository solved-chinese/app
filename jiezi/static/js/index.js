$(document).ready(function () {
    $('#video_image').click(function () {
        video = '<iframe style="width:50vw;height: 27vw; vertical-align: middle" src="' + $(this).attr('data-video') + '"></iframe>';
        $(this).replaceWith(video);
    });
    $("#slideshow > div:gt(0)").hide();
    setInterval(function () {
        $('#slideshow > div:first')
            .fadeOut(1000)
            .next()
            .fadeIn(1000)
            .end()
            .appendTo('#slideshow');
    }, 5000);
});
