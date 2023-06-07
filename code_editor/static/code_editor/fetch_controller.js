function code_editor(content) {
    CodeMirror(document.getElementById('main'), {
        lineNumbers: true,
        tabSize: 2,
        value: content,
        mode: "text/x-csrc",
    });
}

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
            main.innerHTML = '';
            fetchData(file).then(function (data) {
                code_editor(data.file)
                document.getElementById('compile-dropdown').innerHTML = "<a onclick=\"compile(" + file + ")\">Compile</a>";
                document.getElementsByClassName('snippet')[0].innerHTML = "";

                localStorage.setItem('file', data.file);
            }).catch(function (error) {
                console.error(error);
            });
        });
    });

    async function fetchData(file) {
        try {
            const response = await fetch("/code_editor/" + file + "/");

            return await response.json();
        } catch (error) {
            throw new Error('AJAX request failed: ${error}');
        }
    }
});

(function () {
    document.getElementById('main').innerHTML = "";
    let file_data = localStorage.getItem('file');
    let file_id = localStorage.getItem('file_id');
    if (file_data) {
        code_editor(file_data);
        document.getElementById('compile-dropdown').innerHTML = "<a onclick=\"compile(" + file_id + ")\">Compile</a>";
    } else {
        code_editor("");
        document.getElementById('compile-dropdown').innerHTML = "<a href=\"/code_editor/compile/\">No file selected</a>";
    }
})();