function save_z80() {
    let callee_state = document.getElementById("callee");
    let reserve_state = document.getElementById("reserve");
    localStorage.setItem("callee_checked", callee_state.checked);
    localStorage.setItem("reserve_checked", reserve_state.checked);
}

(function () {
    let callee = localStorage.getItem("callee_checked");
    let reserve = localStorage.getItem("reserve_checked");
    if (callee === null) {
        callee = false;
    }
    if (reserve === null) {
        reserve = false;
    }
    if (callee === "true") {
        document.getElementById("callee").checked = callee;
    } else {
        document.getElementById("callee").checked = false;
    }
    if (reserve === "true") {
        document.getElementById("reserve").checked = reserve;
    } else {
        document.getElementById("reserve").checked = false;
    }
})();