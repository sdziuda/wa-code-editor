function add_highlighting() {
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
}

function compile(file_id) {
    fetchCompileData(file_id).then(function (data) {
        let snippet = document.getElementsByClassName('snippet')[0];
        snippet.innerHTML = data;
        add_highlighting();
        localStorage.setItem('compilation', data);
    }).catch(function (error) {
        console.error(error);
    });
}

async function fetchCompileData(file) {
    try {
        const response = await fetch("/code_editor/compile/" + file);
        console.log(response)
        if (!response.ok) {
            throw new Error('AJAX request failed: ' + response.status);
        }

        return await response.text();
    } catch (error) {
        throw new Error('AJAX request failed: ' + error);
    }
}

(function () {
    let file_data = localStorage.getItem('compilation');
    if (file_data) {
        document.getElementsByClassName('snippet')[0].innerHTML = file_data;
        add_highlighting();
    } else {
        document.getElementsByClassName('snippet')[0].innerHTML = "";
    }
})();