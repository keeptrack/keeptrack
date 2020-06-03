function checkboxClicked() {
    var checkbox = window.event.target;
    var name = checkbox.name;
    var row = document.getElementById("equip" + name);
    var disabled = !checkbox.checked;
    
    var children = row.childNodes;

    for (var i = 0; i < children.length; i++) {
        if (children[i].nodeName == "TD") {
            var cellChildren = children[i].childNodes;
            for (var j = 0; j < cellChildren.length; j++) {
                if (cellChildren[j].nodeName == "INPUT"
                    && cellChildren[j].name != name) {
                    cellChildren[j].disabled = disabled;
                }
            }
        }
    }
}

function filterChanged() {
    
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
};
