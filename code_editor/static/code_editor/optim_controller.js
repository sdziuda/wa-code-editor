function save_optim() {
    let speed_state = document.getElementById("speed");
    let reverse_state = document.getElementById("reverse");
    let nolab_state = document.getElementById("nolab");
    localStorage.setItem("speed_checked", speed_state.checked);
    localStorage.setItem("reverse_checked", reverse_state.checked);
    localStorage.setItem("nolab_checked", nolab_state.checked);
}

(function () {
    let speed = localStorage.getItem("speed_checked");
    let reverse = localStorage.getItem("reverse_checked");
    let nolab = localStorage.getItem("nolab_checked");

    if (speed === null) {
        speed = false;
    }
    if (reverse === null) {
        reverse = false;
    }
    if (nolab === null) {
        nolab = false;
    }
    if (speed === "true") {
        document.getElementById("speed").checked = speed;
    } else {
        document.getElementById("speed").checked = false;
    }
    if (reverse === "true") {
        document.getElementById("reverse").checked = reverse;
    } else {
        document.getElementById("reverse").checked = false;
    }
    if (nolab === "true") {
        document.getElementById("nolab").checked = nolab;
    } else {
        document.getElementById("nolab").checked = false;
    }
})();