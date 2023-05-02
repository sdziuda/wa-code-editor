function change_proc() {
    let list = document.getElementById("processor");
    let id = list.options[list.selectedIndex].value;
    document.getElementById("procmcs51").style.display = "none";
    document.getElementById("procz80").style.display = "none";
    document.getElementById("procstm8").style.display = "none";

    document.getElementById("proc" + id).style.display = "block";
}
