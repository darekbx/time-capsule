$(document).on('change', '#browsebutton :file', function () {
    var input = $(this),
        numFiles = input.get(0).files ? input.get(0).files.length : 1,
        label = input.val().replace(/\\/g, '/').replace(/.*\//, '');
    input.trigger('fileselect', [numFiles, label]);
});

$(document).ready(function () {
    $('#browsebutton :file').on('fileselect', function (event, numFiles, label) {
        var input = $(this).parents('.input-group').find(':text'),
            log = numFiles > 1 ? numFiles + ' files selected' : label;

        if (input.length) {
            input.val(log);
        } else {
            if (log) alert(log);
        }

    });
});
$(function () {
    var dirName = $("#dir-name");
    var form;
    var dialog = $("#dialog-create-dir").dialog({
        autoOpen: false,
        height: 156,
        width: 240,
        modal: true,
        buttons: {
            "Create": addDir,
        },
        close: function () {
            form[0].reset();
            dirName.removeClass("ui-state-error");
        }
    })

    function addDir() {
        var valid = dirName.val().length > 0;
        dirName.removeClass("ui-state-error");
        if (valid) {
            $.post("/new-dir", { "name": dirName.val(), "dir": window.location.pathname })
                .done(function () {
                    // Reload
                    window.location.replace(window.location.href);
                })
                .fail(function () {
                    alert("An error occurred during creating new directory.");
                });
            dialog.dialog("close");
        } else {
            dirName.addClass("ui-state-error");
        }
        return valid;
    }

    form = dialog.find("form").on("submit", function (event) {
        event.preventDefault();
        addUser();
    });

    $("#create-dir").button().on("click", function () {
        dialog.dialog("open");
    });
});