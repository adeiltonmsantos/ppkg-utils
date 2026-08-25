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

    // Setting the menu button display
    btn_menu.addEventListener('click', function(){
        menu_container.classList.toggle('visible-collum')
    })

    // Hiding the menu when the mouse is not over it
    menu_container.addEventListener('mouseleave', function(){
        menu_container.classList.remove('visible-collum')
    })

    // Function to build menu items
    function makeMenuItems(menu){
        const h1Menu = document.createElement('h1')
        const ulMenu = document.createElement('ul')
        h1Menu.innerText = menu.label
        menu_container.appendChild(h1Menu)
        menu_container.appendChild(ulMenu)
        let liMenu = null
        menu.items.forEach(item => {
            liMenu = document.createElement('li')
            liMenu.append(item.label)
            ulMenu.appendChild(liMenu)
        });
    }

    // Trying to get menu items
    if (menu_items_url){
        fetch(menu_items_url)
            .then(response => {
                if(!response.ok){
                    throw new Error("Itens de menu não carregados")
                }
                return response.json()
            })
            .then(arrayMenu => {
                const homeMenu = arrayMenu.find(item => item.id === 'main')
                makeMenuItems(homeMenu)
            })
            .catch(error => {
                console.log("JSON carregou mas menu falhou: " + error)
            })
    }



})