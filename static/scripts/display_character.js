$("document").ready(function(){
    $("#speak-button").click(() => {
        $.ajax({
            url: "/learning/getAudio/",
            data: {
              t: $("#character-text").text()
            },
            type: "GET",
            dataType : "json",
        })
            .done(data => {
                console.log(data);
            })

            .fail((jqXhr, textStatus, errorMessage) => {
                console.log("fail ajax" + errorMessage);
            })
    })
})