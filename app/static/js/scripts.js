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

    // Create dir
    var dialog = $("#dialog-create-dir").dialog({
        autoOpen: false,
        height: 160,
        width: 240,
        modal: true,
        buttons: { "Create": addDir, },
        close: function () {
            form[0].reset();
            $("#dir-name").removeClass("ui-state-error");
        }
    })
    var form = dialog.find("form").on("submit", function (event) {
        event.preventDefault();
        addUser();
    });

    function addDir() {
        var valid = $("#dir-name").val().length > 0;
        $("#dir-name").removeClass("ui-state-error");
        if (valid) {
            $.post("/new-dir", { "name": $("#dir-name").val(), "dir": window.location.pathname })
                .done(function () { window.location.replace(window.location.href); })
                .fail(function () { 
                    $("<div>An error occurred during creating new directory.</div>").dialog();
                });
            dialog.dialog("close");
        } else {
            $("#dir-name").addClass("ui-state-error");
        }
        return valid;
    }
    $("#create-dir").button().on("click", function () {
        dialog.dialog("open");
    });

    // Make backup
    var makeBackupDialog = $("#make-backup-dialog").dialog({
        autoOpen: false,
        closeOnEscape: false,
        resizable: false,
        buttons: {
            Cancel: function () { $(this).dialog("close"); }
        }
    });
    $("#make-backup").button().on("click", function () {
        $("#make-backup-progressbar").progressbar({
            value: false
        });
        makeBackupDialog.dialog("open");
        $.post("/backup", function (data) {
            makeBackupDialog.dialog("close");
        })
            .done(function () { window.location.replace(window.location.href); })
            .fail(function () { 
                $("<div>An error occurred during creating new directory.</div>").dialog();
            });
    });

    // Delete file
    $(".row-delete-item").on("click", function () {
        var path = $(this).data('path');
        var name = $(this).data('name')
        var dialog = $("<div>Delete '" + name + "'?</div>");
        $(dialog).dialog({
            resizable: false,
            height: "auto",
            width: 400,
            modal: true,
            buttons: {
                "Delete": function () {
                    $.post("/delete", { "path": path })
                        .done(function () { window.location.replace(window.location.href); })
                        .fail(function () { 
                            $("<div>An error occurred during deleting the file.</div>").dialog();
                        });
                },
                Cancel: function () { $(this).dialog("close"); }
            }
        });
        dialog.dialog("open");
    });

    // Open file
    $(".row-open-item").on("click", function () {
        var path = $(this).data('path');
        var name = $(this).data('name')

        $.post("/open", { "path": path }, function (data) { 
            var data = JSON.parse(data);
            var content;
            
            if (data.type == "text") {
                content = "<pre>" + data.content + "</pre>";
            } else if (data.type == "image") {
                content = "<img src='" + data.path + "' />";
            } else {
                content = "<pre>" + data.type + "</pre>";
            }

            $(content).dialog({
                width: $(window).width() * .8,
                height: $(window).height() * .8,
                modal: true,
                fluid: true, //new option
                resizable: false   
            });

         })
            .fail(function (xhr, status, error) {
                if (status != 200) {
                    $("<div>" + xhr.responseText + "</div>").dialog();
                } else {
                    $("<div>An error occurred during reading the file.</div>").dialog();
                }
            });
    
    });
});