
$(document).ready(function () {
    var url = "http://tts.baidu.com/text2audio?lan=zh&ie=UTF-8&spd=0&text=" + encodeURI( $('.letter').text() );
    var audio = new Audio(url);
    audio.src = url;
    $(".audio").click(function(){
        audio.play();
    });


    $(document).on("submit", "#i_know_this", function (event) {
        event.preventDefault();
        var currentForm = this;
        bootbox.confirm({
            title: "Are you sure?",
            message:"This will remove this character from your library",
            buttons: {
                confirm: {
                    label: 'Yes',
                    className: 'btn-primary'
                },
                cancel: {
                    label: 'No',
                    className: 'btn-primary'
                }
            },
            callback:function(result) {
                if(result){
                    console.log("good");
                    currentForm.submit();
                }
            }
        })
    });
})