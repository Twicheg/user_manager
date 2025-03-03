const placeholder = document.getElementById("url");
const result_column = document.getElementById("result_column");
const post_button = document.getElementById("post_button");
const post_card = document.getElementById("post_card");
const post_form_ul = document.getElementById("form_ul");
const post_form_input = document.getElementById("post_form_input");


placeholder.value = "http://127.0.0.1:8000/names/";
placeholder.style.transition = "2s";
placeholder.style.transform = "2s";

placeholder.addEventListener("click", () => {
    placeholder.style.width = "610px";
    placeholder.style.height = "35px";
})

function GetFunc() {
    post_card.style.display = "none";
    result_column.innerHTML = '';
    result_column.style.display = "inline";
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", placeholder.value, true);
    xmlHttp.responseType = 'json';
    xmlHttp.send();
    xmlHttp.onload = () => {

        if (xmlHttp.readyState == 4 && xmlHttp.status == 200) {
            for (let i = 0; i < xmlHttp.response.length; i++) {

                let child = document.createElement("p");
                child.style.fontSize = "26px";
                child.innerText = "counter: " + xmlHttp.response[i].counter + "\n" + " name: " + xmlHttp.response[i].name;
                result_column.appendChild(child);
                var array = xmlHttp.response[i].country;

                for (let j = 0; j < array.length; j++) {
                    const second_child = document.createElement("p");
                    second_child.style.marginTop = "-16px";
                    second_child.innerText = "country_id: " + array[j].country_id + "\n" + " probability: " + array[j].probability;
                    result_column.appendChild(second_child);
                }

            }
        } else {
            console.log(`Error: ${xmlHttp.status}`);
        }
    };
}

function AddCity() {
    let first_el = document.createElement('li');
    let first_inner_label = document.createElement("label");
    let first_inner_input = document.createElement('input');
    let second_el = document.createElement('li');
    let second_inner_label = document.createElement("label");
    let second_inner_input = document.createElement('input');
    let space = document.createElement('div');

    space.innerText = '----------------------';
    post_form_ul.appendChild(space);

    first_inner_label.innerText = "Country_id";
    first_inner_input.type = 'text';
    first_el.appendChild(first_inner_label);
    first_el.appendChild(first_inner_input);
    second_inner_label.innerText = "Probability";
    second_inner_input.type = 'text';
    second_el.appendChild(second_inner_label);
    second_el.appendChild(second_inner_input);
    post_form_ul.appendChild(first_el);
    post_form_ul.appendChild(second_el);
}

post_button.addEventListener("click", () => {
    result_column.style.display = "none";
    post_card.style.transition = "2s";
    post_card.style.display = "inline-flex";
});

function PostFunc() {
    let outerarr = [];
    let innerarr = [];
    let counter = 0;

    for (let i = 0; i < post_form_ul.children.length; i++) {
        if (post_form_ul.children[i].tagName == "LI") {
            counter += 1;
            if (counter < 3) {
                innerarr.push(post_form_ul.children[i].children[1].value);
            }
            if (counter > 1) {
                let myJson = {"country_id": innerarr[0], "probability": innerarr[1]};
                outerarr.push(myJson);
                counter = 0;
                innerarr = [];
            }
        }
    }

    var xmlHttp = new XMLHttpRequest();
    const final_json = JSON.stringify({"name": post_form_input.value, "country": outerarr});
    xmlHttp.open("POST", placeholder.value, true);
    xmlHttp.setRequestHeader('Content-Type', "application/json");

    xmlHttp.responseType = 'json';

    xmlHttp.send(final_json);


    xmlHttp.onload = () => {
        let response = document.createElement("div");
        response.style.fontSize = "28px";
        response.style.paddingLeft = "40px";
        response.style.color = "blue";
        if (xmlHttp.readyState == 4 && xmlHttp.status == 201) {
            response.innerText="Успешно\n добавлено";
            post_card.appendChild(response);
        } else {
            response.innerText="Ошибка\n"+xmlHttp.status;
            post_card.appendChild(response);
        }
    };
}