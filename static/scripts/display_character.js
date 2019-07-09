$("document").ready(function(){
    let pk = $("meta[name='pk']").attr("content");
    $("#speak-button").click(() => {
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
                    var audio = new Audio('/static/audio/' + pk + '.wav');
                    audio.play();
                } else {
                    $("#audio-error-msg").fadeIn();
                    setTimeout(() => {
                        $("#audio-error-msg").fadeOut()
                    }, 3500);
                }
            })

            .fail((jqXhr, textStatus, errorMessage) => {
                $("#audio-error-msg").fadeIn();
                setTimeout(() => {
                    $("#audio-error-msg").fadeOut()
                }, 3500);
            })
    })
})