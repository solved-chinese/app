/***********************************
  CSRF
***********************************/

var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            console.log('add csrf');
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

/***********************************
  Modal Helper Functions
***********************************/

function showModal(modalId) {
    $('.page-mask').show();
    $(`#${modalId}`).show();
}

function hideModal(modalId) {
    $('.page-mask').hide();
    $(`#${modalId}`).hide();
}


/***********************************
  Search
***********************************/

const MAX_ENTRIES_DISPLAY = 6;
const $source = $('.search-input-wrapper > input');
const $target = $('#search-dropdown-wrapper');

$('.search-form-wrapper').focusout(() => {
    setTimeout(() => {
        $target.html('');
    }, 150);
});

function searchHandler(e) {
    let query = $source.val();
    if (query === '') {
        $target.html('');
        return;
    }

    $.post({
        url: '/content/search/',
        data: {
            keyword: query
        }
    })
    .done(data => {
        $target.empty();
        $('<hr>').appendTo($target);

        if (data.length === 0) {
            $('<div class="error-msg">No Match</div>').appendTo($target);
            return;
        }

        for (let i = 0; i < Math.min(data.length, MAX_ENTRIES_DISPLAY); i++) {
            let char = data[i];
            let targetPk = char.id.toString().padStart(4, '0');
            let entry = `
                <a href='/content/C${targetPk}' class='search-entry-wrapper'>
                    <div class='search-entry'>
                        <span class='character'>${char.chinese}</span>
                        <span class='pinyin'>${char.pinyin.replace(/\s+/g, '')}</span>
                        <p class='definition'>${char.definition_1}
                        </p>
                    </div>
                </a>`;
            // Some pinyins contain whitespaces, hence they are removed here (temporary fix)
            $(entry).appendTo($target);
        }
    })
    .fail((xhr, status, errorThrown) => {
        $target.html('<hr><div class="error-msg">There was a problem connecting with the Solved server</div>');
        return;
    });
}

function toggleSearch() {
    $("#main-navbar #search-input").prop("disabled", (_, val) => {
        return !val;
    });
    $("#main-navbar .navbar-item#search-form").toggleClass("disabled");
}

$source.on('input propertychange', searchHandler);
$source.keypress(e => {
    if (e.keyCode !== 13 || $('.search-entry-wrapper').length === 0) return;
    $('.search-entry-wrapper')[0].click();
});

/***********************************
  Responsive
***********************************/

function mobileMenuToggle() {
    const navItem = $("#main-navbar > .navbar-item#menu");
    const navbar = $("#main-navbar");
    $.merge(navItem, navbar).toggleClass("responsive");
    $("#main-navbar > .navbar-item#menu-toggle").toggleClass("active");
    $("#main-navbar .dropdown-menu").toggleClass("show");
    $("#page-container").toggleClass("inactive");
    toggleSearch();
}

function closeMobileMenu() {
    if ($("#page-container").hasClass("inactive")) {
        mobileMenuToggle();
    }
}