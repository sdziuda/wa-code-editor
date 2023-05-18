function sendStdForm() {
    let form = document.getElementsByName("standard_opt")[0];
    let choice = form.elements["std"].value;
    let csrf = form.elements["csrfmiddlewaretoken"].value;
    sendStdData(choice, csrf).then(function (data) {
    }).catch(function (error) {
        console.error(error);
    });
}

async function sendStdData(choice, csrf) {
    try {
        const response = await fetch("/code_editor/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrf
            },
            body: JSON.stringify({
                "standard_opt": choice
            })
        });
        if (!response.ok) {
            throw new Error('AJAX request failed: ' + response.status);
        }

        return await response.text();
    } catch (error) {
        throw new Error('AJAX request failed: ' + error);
    }
}

function save_optim() {
    let speed_state = document.getElementById("speed");
    let reverse_state = document.getElementById("reverse");
    let nolab_state = document.getElementById("nolab");
    localStorage.setItem("speed_checked", speed_state.checked);
    localStorage.setItem("reverse_checked", reverse_state.checked);
    localStorage.setItem("nolab_checked", nolab_state.checked);
}

function sendOptimForm() {
    let form = document.getElementsByName("optimization_opt")[0];
    let speed = form.elements["speed"].checked;
    let reverse = form.elements["reverse"].checked;
    let nolabel = form.elements["nolab"].checked;
    let csrf = form.elements["csrfmiddlewaretoken"].value;
    sendOptimData(speed, reverse, nolabel, csrf).then(function() {
        save_optim();
    }).catch(function (error) {
        console.error(error);
    });
}

async function sendOptimData(speed, reverse, nolabel, csrf) {
    try {
        const response = await fetch("/code_editor/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrf
            },
            body: JSON.stringify({
                "optimization_opt": {
                    "speed": speed,
                    "reverse": reverse,
                    "nolab": nolabel
                }
            })
        });
        if (!response.ok) {
            throw new Error('AJAX request failed: ' + response.status);
        }

        return await response.text();
    } catch (error) {
        throw new Error('AJAX request failed: ' + error);
    }
}

function sendProcForm() {
    let form = document.getElementsByName("processor_opt")[0];
    let choice = form.elements["proc"].value;
    let csrf = form.elements["csrfmiddlewaretoken"].value;
    sendProcData(choice, csrf).then(function() {
        change_proc();
    }).catch(function (error) {
        console.error(error);
    });
}

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

async function sendProcData(choice, csrf) {
    try {
        const response = await fetch("/code_editor/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrf
            },
            body: JSON.stringify({
                "processor_opt": choice
            })
        });
        if (!response.ok) {
            throw new Error('AJAX request failed: ' + response.status);
        }

        return await response.text();
    } catch (error) {
        throw new Error('AJAX request failed: ' + error);
    }
}

function sendMCS51Form() {
    let form = document.getElementsByName("mcs51_opt")[0];
    let choice = form.elements["mcs51"].value;
    let csrf = form.elements["csrfmiddlewaretoken"].value;
    sendMCS51Data(choice, csrf).then(function (data) {
    }).catch(function (error) {
        console.error(error);
    });
}

async function sendMCS51Data(choice, csrf) {
    try {
        const response = await fetch("/code_editor/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrf
            },
            body: JSON.stringify({
                "mcs51_opt": choice
            })
        });
        if (!response.ok) {
            throw new Error('AJAX request failed: ' + response.status);
        }

        return await response.text();
    } catch (error) {
        throw new Error('AJAX request failed: ' + error);
    }
}

function sendZ80Form() {
    let form = document.getElementsByName("z80_opt")[0];
    let callee = form.elements["callee"].checked;
    let reserve = form.elements["reserve"].checked;
    let csrf = form.elements["csrfmiddlewaretoken"].value;
    sendZ80Data(callee, reserve, csrf).then(function() {
        save_z80();
    }).catch(function (error) {
        console.error(error);
    });
}

function save_z80() {
    let callee_state = document.getElementById("callee");
    let reserve_state = document.getElementById("reserve");
    localStorage.setItem("callee_checked", callee_state.checked);
    localStorage.setItem("reserve_checked", reserve_state.checked);
}

async function sendZ80Data(callee, reserve, csrf) {
    try {
        const response = await fetch("/code_editor/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrf
            },
            body: JSON.stringify({
                "z80_opt": {
                    "callee": callee,
                    "reserve": reserve
                }
            })
        });
        if (!response.ok) {
            throw new Error('AJAX request failed: ' + response.status);
        }

        return await response.text();
    } catch (error) {
        throw new Error('AJAX request failed: ' + error);
    }
}

function sendSTM8Form() {
    let form = document.getElementsByName("stm8_opt")[0];
    let choice = form.elements["stm8"].value;
    let csrf = form.elements["csrfmiddlewaretoken"].value;
    sendSTM8Data(choice, csrf).then(function() {
    }).catch(function (error) {
        console.error(error);
    });
}

async function sendSTM8Data(choice, csrf) {
    try {
        const response = await fetch("/code_editor/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrf
            },
            body: JSON.stringify({
                "stm8_opt": choice
            })
        });
        if (!response.ok) {
            throw new Error('AJAX request failed: ' + response.status);
        }

        return await response.text();
    } catch (error) {
        throw new Error('AJAX request failed: ' + error);
    }
}

(function () {
    change_proc();
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
