document.addEventListener('DOMContentLoaded', function () {
    const delete_list = document.getElementsByClassName('delete');

    Array.from(delete_list).forEach(function (element) {
        let file = element.id;
        let file_type = file.substring(0, 5);
        file = file.substring(5, file.length);

        if (file_type === "file-") {
            element.addEventListener('click', function (event) {
                fetchDeleteFile(file).then(function (data) {
                    document.getElementById("file-list-" + file).style.display = "none";
                }).catch(function (error) {
                    console.error(error);
                });
            });
        } else if (file_type === "dire-") {
            element.addEventListener('click', function (event) {
                fetchDeleteDir(file).then(function (data) {
                    document.getElementById("dir-list-" + file).style.display = "none";
                }).catch(function (error) {
                    console.error(error);
                });
            });
        }
    });

    async function fetchDeleteFile(file) {
        try {
            const response = await fetch("/code_editor/delete_file_no/" + file);
            if (!response.ok) {
                throw new Error('AJAX request failed: ${response.status}');
            }

            return await response.text();
        } catch (error) {
            throw new Error('AJAX request failed: ${error}');
        }
    }

    async function fetchDeleteDir(file) {
        try {
            const response = await fetch("/code_editor/delete_dir_no/" + file);
            if (!response.ok) {
                throw new Error('AJAX request failed: ${response.status}');
            }

            return await response.text();
        } catch (error) {
            throw new Error('AJAX request failed: ${error}');
        }
    }
});