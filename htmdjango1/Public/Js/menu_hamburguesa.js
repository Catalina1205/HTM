document.getElementById("btn_menu").addEventListener("click", mostrar_menu);

document.getElementById("back_menu").addEventListener("click", ocultar_menu);

nav = document.getElementById("nav");
background_menu = document.getElementById("back_menu");

function mostrar_menu(){

    nav.style.left = "0px";
    background_menu.style.display = "block";
}

function ocultar_menu(){

    nav.style.left = "-250px";
    background_menu.style.display = "none";
}


/* Menu desplegable que está dentro del hamburguesa */ 
let listElements = document.querySelectorAll('.list__button--click');

listElements.forEach(listElement => {
    listElement.addEventListener('click', ()=> {
        listElement.classList.toggle('arrow');

        let height = 0;
        let menu = listElement.nextElementSibling;
        if(menu.clientHeight == "0"){
            height = menu.scrollHeight;
        }
        menu.style.height = height+"px";
    })
});