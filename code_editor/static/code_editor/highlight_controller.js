const selectable = document.getElementsByClassName("sec-line");

Array.from(selectable).forEach(function (element) {
    element.addEventListener('mousedown', function (event) {
        if (event.button === 0) {
            element.style.backgroundColor = "red";
            element.style.borderLeft = "5px solid white";
            let line = document.getElementById(element.id.slice(4));
            line.scrollIntoView({ behavior: "smooth", block: "center", inline: "nearest" });
            line.style.backgroundColor = "red";
            line.style.borderLeft = "5px solid white";
        }
    });

    element.addEventListener('mouseup', function (event) {
        element.style.removeProperty("background-color");
        element.style.removeProperty("border-left");
        let line = document.getElementById(element.id.slice(4));
        line.style.removeProperty("background-color");
        line.style.removeProperty("border-left");
    });
});
