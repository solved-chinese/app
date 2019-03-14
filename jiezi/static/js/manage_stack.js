$(document).ready(function () {
    $('#stack_left').load("/accounts/manage_stack_left");
    $('#stack_right').load("/accounts/manage_stack_right");

    $(document).on("click", ".tag_expand_button", function () {
        var pk = $(this).attr('data-tag_pk');
        console.log("expand tag " + pk + typeof pk);
        $(".tag_expand_content[data-tag_pk='" + pk + "']").toggle();
        if ($(this).text() == '+') {
            $(this).text('-')
        } else {
            $(this).text('+')
        }
    });

    $(document).on("click", ".delete_character", function () {
        var tag_pk = $(this).attr('data-tag_pk');
        var character_pk = $(this).attr('data-user_character_pk');
        $("#delete_user_character_tag_pk").attr("value", tag_pk);
        $("#delete_user_character_pk").attr("value", character_pk);
        $("#confirm_character_delete_modal").modal();
    });

    $('#add_new_set_button').click(function () {
        var modal = $('#add_new_set_modal')
        modal.modal();
        modal.find(".modal-body").load('/accounts/manage_stack_new_set');
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

    $("#confirm_character_delete_form").submit(function (event) {
        event.preventDefault();
        $.ajax({
            type: $(this).attr('method'),
            url: $(this).attr('action'),
            data: $(this).serialize(),
            dataType: 'json',
            success: function (data) {
                console.log("delete character data: ");
                console.log(data)
                if (data.tag_pk == '-1')
                    $('.user_character[data-user_character_pk="' + data.character_pk + '"]').hide()
                else
                    $('.user_character[data-user_character_pk="' + data.character_pk + '"][data-tag_pk="' + data.tag_pk + '"]').hide()
                $("#confirm_character_delete_modal").modal('hide')
                $('#confirm_character_delete_form').trigger('reset')
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