document.addEventListener('DOMContentLoaded', function () {
    const file_list = document.getElementsByClassName('file-link');
    const main = document.getElementById('main');

    Array.from(file_list).forEach(function (element) {
        let file = element.id;
        element.addEventListener('click', function (event) {
            localStorage.removeItem('file');
            localStorage.removeItem('file_id');
            localStorage.removeItem('compilation');
            localStorage.setItem('file_id', file);
            fetchData(file).then(function (data) {
                main.innerHTML = data;
                document.getElementById('compile-dropdown').innerHTML = "<a onclick=\"compile(" + file + ")\">Compile</a>";
                document.getElementsByClassName('snippet')[0].innerHTML = "";

                localStorage.setItem('file', data);
            }).catch(function (error) {
                console.error(error);
            });
        });
    });

    async function fetchData(file) {
        try {
            const response = await fetch("/code_editor/" + file + "/");
            if (!response.ok) {
                throw new Error('AJAX request failed: ${response.status}');
            }

            return await response.text();
        } catch (error) {
            throw new Error('AJAX request failed: ${error}');
        }
    }
});

(function () {
    let file_data = localStorage.getItem('file');
    let file_id = localStorage.getItem('file_id');
    if (file_data) {
        document.getElementById('main').innerHTML = file_data;
        document.getElementById('compile-dropdown').innerHTML = "<a onclick=\"compile(" + file_id + ")\">Compile</a>";
    } else {
        document.getElementById('main').innerHTML = "";
        document.getElementById('compile-dropdown').innerHTML = "<a href=\"/code_editor/compile/\">No file selected</a>";
    }
})();