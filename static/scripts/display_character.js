$("document").ready(function(){
    let pk = $("meta[name='pk']").attr("content");
    $.ajax({
        url: "/learning/getAudio/",
        data: {
            t: $("#character-text").text(),
            pk: pk
        },
        type: "GET",
        dataType : "json",
    })
        .done(data => {
            if (data.success) {
                var audio = $("#audio-ctrl");
                audio.attr("src", "/media/audio/"+pk+".mp3");
            }
        })

        .fail((jqXhr, textStatus, errorMessage) => {
            $("#audio-error-msg").fadeIn();
            setTimeout(() => {
                $("#audio-error-msg").fadeOut();
        }, 3500);
    });
});
