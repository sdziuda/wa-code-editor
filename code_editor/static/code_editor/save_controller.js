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

function save_file(file) {
    let main = document.getElementById('main');
    let save = document.getElementById('save');
    let csrf = save.elements["csrfmiddlewaretoken"].value;
    saveData(file, csrf).then(function (data) {
        main.innerHTML = '';
        code_editor(data.file);
    }).catch(function (error) {
        console.error(error);
    });
}

async function saveData(file, csrf) {
    try {
        let file_content = document.getElementsByClassName('CodeMirror')[0].CodeMirror.getValue();
        const response = await fetch("/code_editor/save_file/" + file, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrf
            },
            body: JSON.stringify({
                "file_content": file_content
            })
        });
        if (!response.ok) {
            throw new Error('AJAX request failed: ' + response.status);
        }

        return await response.json();
    } catch (error) {
        throw new Error('AJAX request failed: ' + error);
    }
}