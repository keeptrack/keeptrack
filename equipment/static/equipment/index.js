const types = ["category", "brand", "name", "condition", "value",
               "storage_location", "next_hire_date", "hire_price", "notes"];

var lastUid;

var selectedCount = 0;
var selectedMarkedCount = 0;

function changeRowDisable(checkboxName, row, disabled) {
    var children = row.childNodes;

    for (var i = 0; i < children.length; i++) {
        if (children[i].nodeName == "TD") {
            var cellChildren = children[i].childNodes;
            for (var j = 0; j < cellChildren.length; j++) {
                if (cellChildren[j].nodeName == "INPUT"
                    && cellChildren[j].id != checkboxName) {
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

function checkboxClicked() {
    var checkbox = window.event.target;
    var name = checkbox.id;
    var row = document.getElementById("equip" + name);
    var disabled = !checkbox.checked;
    
    changeRowDisable(name, row, disabled);
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
                input.min = 0;
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

            selectedCount -= 1;
            updateRemoveRestoreButtons();
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

function getUpdatedRows() {
    var rows = document.getElementsByTagName("TR");
    var rowsToReturn = [];

    for (var i = 0; i < rows.length; i++) {
        if (rows[i].id.includes("equip")) {
            var classList = rows[i].classList;
            if (classList.contains("updated") ||
                classList.contains("deleted") ||
                classList.contains("new")) {
                rowsToReturn.push(rows[i]);
            }
        }
    }

    return rowsToReturn;
}

function saveChangesClicked() {
    var rows = getUpdatedRows();
    var assets = [];

    rows.forEach(function (row, index) {
        object = {};

        var classList = row.classList;
        if (classList.contains("deleted")) {
            object["action"] = "delete";
        } else if (classList.contains("updated")) {
            object["action"] = "update";
        } else if (classList.contains("new")) {
            object["action"] = "new";
        } else {
            return;
        }
        
        object["uid"] = row.getElementsByTagName("SPAN")[0].innerText
            .replace(" ", "");

        var inputs = row.getElementsByTagName("INPUT");

        var typeIndex = 0;
        for (var i = 1; i < inputs.length; i++, typeIndex++) {
            var type = types[typeIndex];
            
            if (type == "next_hire_date") {
                type = types[++typeIndex];
            }
            
            object[type] = inputs[i].value;
        }

        assets.push(object);
    });

    if (assets.length > 0) {
        saveChanges(JSON.stringify(assets));
    }
}

function unmarkAllRows() {
    var rows = document.getElementsByTagName("TR");
    var rowsToDelete = []

    for (var i = 0; i < rows.length; i++) {
        if (rows[i].id.includes("equip")) {
            var selected = rows[i].children[0].children[0].checked;
            if (rows[i].classList.contains("deleted")) {
                rowsToDelete.push(rows[i]);
            } else {
                rows[i].classList.remove("updated");
                rows[i].classList.remove("new");

                var checkbox = rows[i].children[0].children[0];
                checkbox.checked = false;
                changeRowDisable(checkbox.id, rows[i], true);
            }

            if (selected) {
                selectedMarkedCount -= 1;
            }
        }
    }

    rowsToDelete.forEach(function (row, item) {
        row.parentNode.removeChild(row);
    });

    $("#asset_table").trigger("update");
    updateRemoveRestoreButtons();
}

function saveChanges(jsonRequest) {
    var request = new XMLHttpRequest();
    request.onreadystatechange = function() {
        if (request.readyState != XMLHttpRequest.DONE) {
            return;
        }

        if (request.status == 200) {
            unmarkAllRows();
        } else {
            alert("Error!");
        }
    };
    request.open("POST", "update");
    request.setRequestHeader("X-CSRFToken",
                             document.getElementById("csrf").value)
    request.send(jsonRequest);
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

    document.getElementById("add_asset")
        .addEventListener("click", addAssetClicked);
    document.getElementById("remove_asset")
        .addEventListener("click", removeAssetClicked);
    document.getElementById("restore_asset")
        .addEventListener("click", restoreAssetClicked);
    document.getElementById("save_changes")
        .addEventListener("click", saveChangesClicked);

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
