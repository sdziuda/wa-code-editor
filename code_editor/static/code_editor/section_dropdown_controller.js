function sec(id) {
    let con = document.getElementById("con" + id);
    if (con.style.display === "none") {
        con.style.display = "block";
    } else {
        con.style.display = "none";
    }

    let collapsed = 0;
    let list = document.getElementsByClassName("sec-con");
    for (let i = 0; i < list.length; i++) {
        if (list[i].style.display === "none") {
            collapsed++;
        }
    }

    if (collapsed === list.length) {
        document.getElementById("col-or-exp").innerText = "Expand all";
    } else {
        document.getElementById("col-or-exp").innerText = "Collapse all";
    }
}

function col_or_exp() {
    let list = document.getElementsByClassName("sec-con");
    let collapsed = 0;
    for (let i = 0; i < list.length; i++) {
        if (list[i].style.display === "none") {
            collapsed++;
        }
    }

    if (collapsed === list.length) {
        for (let i = 0; i < list.length; i++) {
            list[i].style.display = "block";
        }
        document.getElementById("col-or-exp").innerText = "Collapse all";
    } else {
        for (let i = 0; i < list.length; i++) {
            list[i].style.display = "none";
        }
        document.getElementById("col-or-exp").innerText = "Expand all";
    }
}
