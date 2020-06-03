const types = ["category", "brand", "name", "condition", "value",
               "storage_location", "next_hire_date", "hire_price", "notes"];

var lastUid;

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
    
    var table = document.getElementById("asset_table");
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

            cell.appendChild(input);
        } else {
            var span = document.createElement("span");
            span.name = "next_hire_date";
            span.innerText = "None";

            cell.appendChild(span);
        }
        
        tableRow.appendChild(cell);
    });

    table.appendChild(tableRow);
}

window.onload = function () {
    var inputs = document.getElementsByTagName("INPUT");

    for (var i = 0; i < inputs.length; i++) {
        if (inputs[i].type == "checkbox") {
            inputs[i].addEventListener("click", checkboxClicked);
        } else if (inputs[i].className == "filter") {
            inputs[i].addEventListener("change", filterChanged);
        }
    }

    document.getElementById("add_asset").addEventListener("click", addAssetClicked);

    lastUid = parseInt(document.getElementById("last_uid").value);
};
