/*
Set default values for errors and loading content
 */
document.addEventListener('DOMContentLoaded', function() {
    let n = document.getElementById('to_display').getAttribute('data-last');
    loadContainer(n);
});

/*
Functionality that adds and removes list items for names
when the number of people gets changed
*/
function loadContainer(n) {
    if (n == 0) return;
    let parent = document.getElementById("container");
    let count = parent.childElementCount;
    if (count > n) {
        for (let i = count - 1; i >= n; i--) {
            let child = document.getElementById("name" + `${i}`);
            parent.removeChild(child);
        }
    } else {
        for (let i = count; i < n; i++) {
            let child = document.createElement("input");
            child.name = "name" + `${i}`;
            child.id = "name" + `${i}`;
            child.type = "name";
            child.placeholder = "person " + `${i + 1}`;
            child.value = "person " + `${i + 1}`;
            parent.appendChild(child);
            document.getElementById(child.id).addEventListener('click', function () {
                this.select();
            });
        }
    }
}

/*
Displays the list of names if the number of people is greater than 0
so that users can enter custom names
 */
function showDiv(divId, element) {
    let n = element.value;
    document.getElementById(divId).style.display = n != 0 ? 'block' : 'none';
    loadContainer(n);
}

/*
removes error if there is error
*/
function removeError(element) {
    if (element.classList.contains('error')) {
        element.classList.remove('error');
    }
}

/*
will change color if bill image received
 */
function billReceived() {
    let uploader = document.getElementById('billImg');
    let label = document.getElementById('bill_label');
    let text = document.getElementById('label_text');
    if (uploader.files.length > 0) {
        label.textContent = 'file received';
        label.classList.add('received');
    }
}


