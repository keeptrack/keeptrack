const types = ["category", "brand", "name", "condition", "value",
               "storage_location", "next_hire_date", "hire_price", "notes"];

var lastUid;

var selectedCount = 0;
var selectedMarkedCount = 0;

function checkboxClicked() {
    var checkbox = window.event.target;
    var name = checkbox.id;
    var row = document.getElementById("equip" + name);
    var disabled = !checkbox.checked;
    
    var children = row.childNodes;

    for (var i = 0; i < children.length; i++) {
        if (children[i].nodeName == "TD") {
            var cellChildren = children[i].childNodes;
            for (var j = 0; j < cellChildren.length; j++) {
                if (cellChildren[j].nodeName == "INPUT"
                    && cellChildren[j].id != name) {
                    cellChildren[j].disabled = disabled;
                }
            }
        }
    }

    var num = disabled ? -1 : 1;

    if (row.classList.contains("deleted")) {
        selectedMarkedCount += num;
    } else {
        selectedCount += num;
    }

    updateRemoveRestoreButtons();
}

function updateRemoveRestoreButtons() {
    var removeButton = document.getElementById("remove_asset");
    var restoreButton = document.getElementById("restore_asset");

    removeButton.disabled = selectedCount <= 0;
    restoreButton.disabled = selectedMarkedCount <= 0;
}

function matches(input, value) {
    if (input.tagName == "SPAN") {
        return input.innerText.toLowerCase().includes(value.toLowerCase());
    } else if (input.type == "number") {
        return input.value == value;
    } else {
        return input.value.toLowerCase().includes(value.toLowerCase());
    }
}

function filterChanged() {
    var inputsChanged = false;
    
    types.forEach(function (type, index) {
        var inputs = document.getElementsByName(type);
        var query = inputs[0].value;

        if (query == "") {
            return;
        }
        
        for (var i = 1; i < inputs.length; i++) {
            if (!inputsChanged
                || inputs[i].parentNode.parentNode.style.display != "none") {
                if (matches(inputs[i], query)) {
                    inputs[i].parentNode.parentNode.style.display =
                        "table-row";
                } else {
                    inputs[i].parentNode.parentNode.style.display = "none";
                }
            }
        }
        
        inputsChanged = true;
    });

    var addButton = document.getElementById("add_asset");
    
    if (!inputsChanged) {
        var inputs = document.getElementsByTagName("TR");
        for (var i = 0; i < inputs.length; i++) {
            inputs[i].style.display = "table-row";
        }

        addButton.disabled = false;
    } else {
        addButton.disabled = true;
    }
}

function addAssetClicked() {
    var uid = lastUid + 1;
    lastUid = uid;
    
    var tableRow = document.createElement("tr");
    tableRow.id = "equip" + uid;

    var firstCell = document.createElement("td");
    
    var checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.id = uid;
    checkbox.checked = true;
    checkbox.addEventListener("click", checkboxClicked);

    var idSpan = document.createElement("span");
    idSpan.innerText = " " + uid;

    firstCell.appendChild(checkbox);
    firstCell.appendChild(idSpan);

    tableRow.appendChild(firstCell);

    types.forEach(function (type, index) {
        var cell = document.createElement("td");

        if (type != "next_hire_date") {
            var input = document.createElement("input");
            input.name = type;

            if (type == "value" || type == "hire_price") {
                input.type = "number";
                input.value = 0;
            } else {
                input.type = "text";
                input.value = "";
            }

            input.addEventListener("change", update);

            cell.appendChild(input);
        } else {
            var span = document.createElement("span");
            span.name = "next_hire_date";
            span.innerText = "None";

            cell.appendChild(span);
        }
        
        tableRow.appendChild(cell);
    });

    tableRow.classList.add("new");

    $row = $(tableRow);
    $("#asset_table").find("tbody").append($row).trigger("addRows", [$row, false]);

    selectedCount += 1;
    updateRemoveRestoreButtons();
}

function getSelectedRows() {
    var rows = document.getElementsByTagName("TR");
    var rowsToReturn = [];

    for (var i = 0; i < rows.length; i++) {
        if (rows[i].id.includes("equip")
           && rows[i].children[0].children[0].checked) {
            rowsToReturn.push(rows[i]);
        }
    }

    return rowsToReturn;
}

function removeAssetClicked() {
    var rows = getSelectedRows();

    rows.forEach(function (row, index) {
        if (row.classList.contains("new")) {
            document.getElementsByTagName("TBODY")[0].removeChild(row);
            $("#asset_table").trigger("update");
        } else if (!row.classList.contains("deleted")) {
            row.classList.add("deleted");
            selectedCount -= 1;
            selectedMarkedCount += 1;
            updateRemoveRestoreButtons();
        }
    });
}

function restoreAssetClicked() {
    var rows = getSelectedRows();

    rows.forEach(function (row, index) {
        if (row.classList.contains("deleted")) {
            row.classList.remove("deleted");
            selectedCount += 1;
            selectedMarkedCount -= 1;
            updateRemoveRestoreButtons();
        }
    });
}

function update() {
    $("#asset_table").trigger("update");
    var row = window.event.target.parentNode.parentNode;
    if (!row.classList.contains("new")) {
        row.classList.add("updated");
    }
}

window.onload = function () {
    var inputs = document.getElementsByTagName("INPUT");

    for (var i = 0; i < inputs.length; i++) {
        if (inputs[i].type == "checkbox") {
            inputs[i].addEventListener("click", checkboxClicked);
        } else if (inputs[i].className == "filter") {
            inputs[i].addEventListener("change", filterChanged);
        } else {
            inputs[i].addEventListener("change", update);
        }
    }

    document.getElementById("add_asset").addEventListener("click", addAssetClicked);
    document.getElementById("remove_asset").addEventListener("click", removeAssetClicked);
    document.getElementById("restore_asset").addEventListener("click", restoreAssetClicked);

    lastUid = parseInt(document.getElementById("last_uid").value);

    $.tablesorter.addParser({
        id: "input-text",
        format: function(s, table, cell, cellIndex) {
            return $("input", cell).val();
        },
        type: "text"
    });

    $.tablesorter.addParser({
        id: "input-num",
        format: function(s, table, cell, cellIndex) {
            return $("input", cell).val();
        },
        type: "numeric"
    });
        
    $("#asset_table").tablesorter();
};
