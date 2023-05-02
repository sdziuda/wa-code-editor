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
    localStorage.setItem('tab', '1');
})();