function code_editor(content) {
    let old_editor = document.getElementsByClassName('CodeMirror')[0];
    if (old_editor) {
        old_editor.remove();
    }

    CodeMirror.fromTextArea(document.getElementById('main'), {
        lineNumbers: true,
        tabSize: 2,
        mode: "text/x-csrc",
    }).setValue(content);

    localStorage.setItem('file', content);
}

document.addEventListener('DOMContentLoaded', function () {
    const file_list = document.getElementsByClassName('file-link');

    Array.from(file_list).forEach(function (element) {
        let file = element.id;
        element.addEventListener('click', function (event) {
            localStorage.removeItem('file');
            localStorage.removeItem('file_id');
            localStorage.removeItem('compilation');
            localStorage.setItem('file_id', file);
            fetchData(file).then(function (data) {
                code_editor(data.file)
                document.getElementById('compile-dropdown').innerHTML = "<a onclick=\"compile(" + file + ")\">Compile</a>";
                document.getElementById('save-dropdown').innerHTML = "<a onclick=\"save_file(" + file + ")\">Save File</a>";
                document.getElementsByClassName('snippet')[0].innerHTML = "";
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
    let file_data = localStorage.getItem('file');
    let file_id = localStorage.getItem('file_id');
    if (file_data) {
        code_editor(file_data);
        document.getElementById('compile-dropdown').innerHTML = "<a onclick=\"compile(" + file_id + ")\">Compile</a>";
        document.getElementById('save-dropdown').innerHTML = "<a onclick=\"save_file(" + file_id + ")\">Save File</a>";
    } else {
        code_editor("");
        document.getElementById('compile-dropdown').innerHTML = "<a href=\"/code_editor/compile/\">No file selected</a>";
        document.getElementById('save-dropdown').innerHTML = "<a>No file selected</a>";
    }
})();