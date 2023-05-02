function change_proc() {
    let list = document.getElementById("id_proc");
    let id = list.options[list.selectedIndex].value;
    if (id === null) {
        id = "mcs51";
    }
    document.getElementById("procmcs51").style.display = "none";
    document.getElementById("procz80").style.display = "none";
    document.getElementById("procstm8").style.display = "none";

    document.getElementById("proc" + id).style.display = "block";
}

(function () {
    change_proc();
})();
