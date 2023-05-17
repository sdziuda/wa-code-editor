function change_tab(i) {
    localStorage.setItem('tab', i);
    let bgcolor = getComputedStyle(document.documentElement).getPropertyValue('--navbar-color');
    let bgcolor_act = getComputedStyle(document.documentElement).getPropertyValue('--snippet-color');

    for (let j = 1; j <= 4; j++) {
        document.getElementById("bar" + j).style.backgroundColor = bgcolor;
        document.getElementById("tab" + j).style.display = "none";
    }

    document.getElementById("bar" + i).style.backgroundColor = bgcolor_act;
    document.getElementById("tab" + i).style.display = "block";
}

(function () {
    if (localStorage.getItem('tab') != null) {
        change_tab(localStorage.getItem('tab'));
    } else {
        change_tab(1);
    }
})();