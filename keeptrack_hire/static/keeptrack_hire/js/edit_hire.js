// Show and hide add item buttons.
$("#btn-add-asset").click(function() {
    if ($("#frm-add-asset").is(":visible")) {
        $("#frm-add-asset").hide();
    } else {
        $("#frm-add-asset").show();
        $("#frm-add-custom").hide();
    }
});

$("#btn-add-custom").click(function() {
    if ($("#frm-add-asset").is(":visible")) {
        $("#frm-add-custom").hide();
    } else {
        $("#frm-add-asset").hide();
        $("#frm-add-custom").show();
    }
});

$("#frm-add-asset").submit(function(e) {
    e.preventDefault();  // Don't refresh the site.

    var form = $(this);
    var url = $(this).attr("action")
    var csrftoken = $("[name=csrfmiddlewaretoken]").val();

    // FIXME: Placeholder value for testing.
    $("#asset-id").val("1");

    $.ajax({
        type: "PUT",
        url: url,
        headers:{
            "X-CSRFToken": csrftoken
        },
        data: $("#frm-add-asset").serialize(),
        success: function(data, textStatus, jqXHR) {
            // $("#frm-add-asset").find("input").not("[type=submit]").val("")
            location.reload();
        }
    });
})

$(".basicAutoSelect").autoComplete({
    formatResult: function(item) {
        return {
            id: item.id,
            text: `${item.category} / ${item.brand} / ${item.name}`,
            html: [
                $('<span>').attr('data-toggle', 'tooltip')
                           .attr('title', `Condition: ${item.condition.toUpperCase()}`)
                           .text(`${item.category} / ${item.brand} / ${item.name}`)
                           .tooltip()
            ]
        };
    }
});

$(".basicAutoSelect").on("autocomplete.select", function(evt, item) {
    try {
        $("input[name=asset-id]").val(item.id);
        $("input[type=submit]", $("#frm-add-asset")).prop("disabled", false);
    } catch(err) {}
});

$(".basicAutoSelect").on("click", function() {
    console.log("clicked me");
    $(".basicAutoSelect").autoComplete("show");
});
