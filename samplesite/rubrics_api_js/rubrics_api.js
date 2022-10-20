const domain = 'http://127.0.0.1:8000/';


const username = 'username';
const password = 'password';
const credentials = window.btoa(username + ':' + password);

let list = document.getElementById('list');
let listLoader = new XMLHttpRequest();

listLoader.addEventListener('readystatechange', () => {
    if (listLoader.readyState == 4) {
        if (listLoader.status == 200) {
            let data = JSON.parse(listLoader.responseText);
            let s = '<ul>';
            for (let i = 0; i < data.length; i++) {
                let d = data[i];
                s += '<li>' + d.name + ' <a href="' + domain + 'bboard/api/rubrics/' + d.id + '" class="detail">Вывести </a><a href="' + domain + 'bboard/api/rubrics/' + d.id + '" class="delete">Удалить </a></li>';
            }
            s += '</ul>';
            list.innerHTML = s;
            let links = list.querySelectorAll('ul li a.detail');
            links.forEach((link) => {link.addEventListener('click', rubricLoad)});
            links = list.querySelectorAll('ul li a.delete');
            links.forEach((link) => {link.addEventListener('click', rubricDelete)});
        } else
            window.alert(listLoader.statusText);
}
}) ;



let id = document.getElementById('id');
let nameForm = document.getElementById('name');
let rubricLoader = new XMLHttpRequest();

rubricLoader.addEventListener('readystatechange', () => {
    if (rubricLoader.readyState == 4) {
        if (rubricLoader.status == 200) {
            let data = JSON.parse(rubricLoader.responseText);
            id.value = data.id;
            nameForm.value = data.name;
        } else
        window.alert(rubricLoader.statusText);
    }});

let rubricUpdater = new XMLHttpRequest();

rubricUpdater.addEventListener('readystatechange', () => {
    if (rubricLoader.readyState == 4) {
        if ((rubricLoader.status == 200) || (rubricLoader.status == 201)) {
            listLoad();
            console.log(nameForm)
            nameForm.form.reset();
            id.value = '';
        } else
        window.alert(rubricUpdater.statusText)
    }}
)

nameForm.form.addEventListener('submit', (e) => {
    e.preventDefault();
    let vid = id.value, url, method;
    if (vid) {
        console.log(vid)
        url = 'bboard/api/rubrics/' + vid;
        method = 'PUT';
    } else {
        url = 'bboard/api/rubrics';
        method = 'POST';
    }
    let data = JSON.stringify({id: vid, name: nameForm.value})
    console.log(data)
    rubricUpdater.open(method, domain + url, true);
    rubricUpdater.setRequestHeader('Content-Type', 'application/json');
    rubricUpdater.send(data)
}
)

let rubricDeleter = new XMLHttpRequest();
rubricDeleter.addEventListener('readystatechange', () => {
    if (rubricDeleter.readyState == 4){
        if (rubricDeleter.status == 204) {
            listLoad()
        } 
        else {
            window.alert(rubricDeleter.statusText)
        }
    }
})


function rubricDelete(e) {
    e.preventDefault()
    rubricDeleter.open('DELETE', e.target.href, true)
    rubricDeleter.send()
}


function rubricLoad(e) {
    e.preventDefault()
    rubricLoader.open('GET', e.target.href, true);
    rubricLoader.setRequestHeader('Authorization', 'Basic ' + credentials)
    console.log('Authorization', 'Basic' + credentials)
    rubricLoader.send()
}

function listLoad() {
    listLoader.open('GET', domain + 'bboard/api/rubrics', true);
    listLoader.send();
    }

listLoad();