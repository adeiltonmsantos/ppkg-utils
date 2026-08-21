document.addEventListener('DOMContentLoaded', function(){
    // Menu icon
    const btn_menu = document.querySelector('.menu-main-container img')
    // Menu container
    const menu_container = document.querySelector('.menu-container')
    // Element with profile user and menu items URL
    const menu_items_container = document.querySelector('#items')
    // Menu items URL
    const menu_items_url = menu_items_container.value
    // User profile (0: common user; 1: superuser)
    const user_profile = menu_items_container.dataset.spr
    // Original menu items object
    let menuItemsObj = 'Nada ainda'

    // Setting the menu button display
    btn_menu.addEventListener('click', function(){

    })


    // Trying to get menu items
    if (menu_items_url){
        menuItemsObj = fetch(menu_items_url)
            .then(response => {
                if(!response.ok){
                    throw new Error("Itens de menu não carregados")
                }
                return response.json()
            })
            .catch(error => {
                console.log("Itens de menu não foram carregados")
            })
    }



})