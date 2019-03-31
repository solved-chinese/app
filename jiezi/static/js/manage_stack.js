$(document).ready(function () {
    $('#stack_left').load("/accounts/manage_stack_left");

    $(document).on("click", ".tag_expand_button", function () {
        var pk = $(this).attr('data-tag_pk');
        console.log("expand tag " + pk + typeof pk);
        $(".tag_expand_content[data-tag_pk='" + pk + "']").toggle();
        if ($(this).text() == '+') {
            $(this).text('▼')
        } else {
            $(this).text('▼')
        }
    });

    //for selecting preview
    $(document).on("click", ".show_preview", function () {
        console.log('get');
        var pk = $(this).parent().parent().attr('data-character_pk');
        console.log("pk is " + pk);
        pk = ("000" + pk).slice(-4)
        console.log("pk is " + pk);
        $('#stack_right').load("/learning/C" + pk + "_pure");
    });

    $(document).on("click", ".delete_character", function () {
        var tag_pk = $(this).attr('data-tag_pk');
        var character_pk = $(this).attr('data-user_character_pk');
        $("#delete_user_character_tag_pk").attr("value", tag_pk);
        $("#delete_user_character_pk").attr("value", character_pk);
        $("#confirm_character_delete_modal").modal();
    });

    $("#confirm_character_delete_form").submit(function (event) {
        event.preventDefault();
        $.ajax({
            type: $(this).attr('method'),
            url: $(this).attr('action'),
            data: $(this).serialize(),
            dataType: 'json',
            success: function (data) {
                console.log("delete character data: ");
                console.log(data);
                if (data.tag_pk == '-1')
                    $('.user_character[data-user_character_pk="' + data.character_pk + '"]').hide();
                else
                    print('this is delete from lib');
                $('.user_character[data-user_character_pk="' + data.character_pk + '"][data-tag_pk="' + data.tag_pk + '"]').hide();
                $("#confirm_character_delete_modal").modal('hide');
                $('#confirm_character_delete_form').trigger('reset');
            },
            error: function (xhr, errmsg, err) {
                $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: " + errmsg +
                    " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
        return false;
    });

    $(document).on("click", ".delete_tag", function () {
        var tag_pk = $(this).attr('data-tag_pk');
        $("#delete_tag_pk").attr("value", tag_pk);
        $("#confirm_tag_delete_modal").modal();
    });
    $("#confirm_tag_delete_form").submit(function (event) {
        event.preventDefault();
        $.ajax({
            type: $(this).attr('method'),
            url: $(this).attr('action'),
            data: $(this).serialize(),
            dataType: 'json',
            success: function (data) {
                console.log(data);
                $('#stack_left').load("/accounts/manage_stack_left");
                $("#confirm_tag_delete_modal").modal('hide')
                $('#confirm_tag_delete_form').trigger('reset')
            },
            error: function (xhr, errmsg, err) {
                $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: " + errmsg +
                    " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
        return false;
    });


    $('#add_new_set_button').click(function () {
        var modal = $('#add_new_set_modal')
        modal.modal();
        modal.find(".modal-body").load('/accounts/manage_stack_new_set_modal');
    })
    $(document).on('click', 'button[name="add_set_pk"]', function () {
        var button = $(this)
        var form = $('#add_new_set_form');
        var data = form.serialize() + "&add_set_pk=" + button.val();
        console.log(data)
        $.ajax({
            type: form.attr('method'),
            url: form.attr('action'),
            data: data,
            dataType: 'json',
            success: function (data) {
                console.log(data);
                $('#stack_left').load("/accounts/manage_stack_left");
                button.hide();
            },
            error: function (xhr, errmsg, err) {
                $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: " + errmsg +
                    " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
        return false;
    });
});