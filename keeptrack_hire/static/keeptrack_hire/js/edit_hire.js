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
    if ($("#frm-add-custom").is(":visible")) {
        $("#frm-add-custom").hide();
    } else {
        $("#frm-add-asset").hide();
        $("#frm-add-custom").show();
    }
});

$("#frm-add-asset").submit(function(e) {
    e.preventDefault();  // Don't refresh the site.

    var form = $(this);
    var url = form.attr("action")
    var csrftoken = $("[name=csrfmiddlewaretoken]", form).val();

    $.ajax({
        type: "PUT",
        url: url,
        headers:{
            "X-CSRFToken": csrftoken
        },
        data: form.serialize(),
        success: function(data, textStatus, jqXHR) {
            location.reload();
        }
    });
})

$("#frm-add-custom").submit(function(e) {
    e.preventDefault();  // Don't refresh the site.

    var form = $(this);
    var url = form.attr("action")
    var csrftoken = $("[name=csrfmiddlewaretoken]", form).val();

    console.log(`Sending PUT request to ${url}`);

    $.ajax({
        type: "PUT",
        url: url,
        headers:{
            "X-CSRFToken": csrftoken
        },
        data: form.serialize(),
        success: function(data, textStatus, jqXHR) {
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
