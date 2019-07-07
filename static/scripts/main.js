
var app = new Vue({
  el: '#navbar',
  data: {
    username: 'George Yu'
  }
})

var app = new Vue({
  el: '#page-container',
  data: {
    firstName: 'George',
    streakDayCount: 3,
    streakMonth: 'March'
  }
})

$(document).ready(() => {
  const $source = $(".search-form-wrapper > input[name='keyword']");
  const $target = $("#search-dropdown-wrapper");
  $source.blur(() => {
    $target.html("");
  })
  const searchHandler = () => {
    keyword = $source.val();
    if (keyword != "") {
      $.ajax({
          url: "/learning/search/",
  
          data: {
            keyword: keyword
          },
  
          type: "POST",
  
          dataType : "json",
      })
        .done(json => {
          if (json.characters.length == 0) {
            $target.html("<hr><div class='error-msg'>NO MATCH</div>");
          } else {
            $target.html("<hr>");
            for (let i=0; i <= (json.characters.length>6 ? 6:json.characters.length); i++){
              let character = json.characters[i].fields;
              let target_pk = ("0000" + json.characters[i].pk).slice(-4);
              let entry = "<a href='/learning/C"+target_pk+"' class='search-entry-wrapper'><div class='search-entry'><h4>"+character.chinese+"<small>["+character.pinyin.replace(/\s+/g, '')+"]</small></h4> \
                <p>"+character.definition_1+"<br><span>"+character.explanation_2+"</span></p></div></a>"; 
                // The replace method is to temporarily remove the space in some pinyin entries until this issue is solved in the database.
              $(entry).appendTo($target);
            }
          }
        })
  
        .fail((xhr, status, errorThrown) => {
          $target.html("<hr><div class='error-msg'>There was a problem connecting with the Solved server</div>");
        })
    } else {
      $target.html("")
    }
  }
  
  $source.on("input propertychange", searchHandler);
}) 
