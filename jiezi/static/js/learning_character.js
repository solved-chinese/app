
$(document).ready(function () {
    var url = "http://tts.baidu.com/text2audio?lan=zh&ie=UTF-8&spd=0&text=" + encodeURI( $('.letter').text() );
    var audio = new Audio(url);
    audio.src = url;
    $(".audio").click(function(){
        audio.play();
    });
})