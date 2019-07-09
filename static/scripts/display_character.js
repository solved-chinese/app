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
                }
                console.log(data.success);
            })

            .fail((jqXhr, textStatus, errorMessage) => {
                console.log("fail ajax" + errorMessage);
            })
    })
})