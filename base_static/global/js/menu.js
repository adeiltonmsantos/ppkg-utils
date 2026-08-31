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
    const user_profile = parseInt(menu_items_container.dataset.spr)
    
    // Flag to inform if menu is beeing rebuilded
    let isRebuilding = false

    // Setting the menu button display
    btn_menu.addEventListener('click', function(){
        menu_container.classList.toggle('visible-collum')
    })


    // Hiding the menu when the mouse is not over it
    menu_container.addEventListener('mouseleave', function(){
        if(isRebuilding)
            return
        menu_container.classList.remove('visible-collum')
    })

    // Setting isRebuilding flag to false when user puts mouse over any menu item
    menu_container.addEventListener('mouseover', function(){
        isRebuilding = false
    })


    // Function to build menu items. Must be given an object menu and user profile
    // (1: superuser, 0: common user)
    function makeMenuItems(menu, user_profile){
        // Cleaning menu container
        menu_container.innerHTML = ""
        const h1Menu = document.createElement('h1')
        const ulMenu = document.createElement('ul')
        h1Menu.innerText = menu.label
        menu_container.appendChild(h1Menu)
        menu_container.appendChild(ulMenu)
        let liMenu = null
        let linkMenu = null
        let profileUserItem = null
        menu.items.forEach(item => {
            profileUserItem = parseInt(item.profile_super)
            if(user_profile === 1 || (user_profile === 0 && profileUserItem == 0)){
                // Creating menu item (li)
                liMenu = document.createElement('li')
    
                // Menu item must be a link to another page
                if (item.url != ""){
                    // Creating link (a)
                    linkMenu = document.createElement('a')
                    linkMenu.append(item.label)
                    // Defining target of item menu 
                    linkMenu.setAttribute('href', item.url)
                    // Defining attribute 'data-type-item' as 'link'
                    linkMenu.setAttribute('data-type-item', 'link')
                    // Adding menu item to link
                    liMenu.append(linkMenu)
                    // Adding item to menu container
                    ulMenu.appendChild(liMenu)
                }
                // Menu item is not a link to another page. Its a link to other menu items
                else{
                    // Appending label in menu item
                    liMenu.append(item.label)
                    // Defining attribute 'data-type-item' as 'menu'
                    liMenu.setAttribute('data-type-item', 'menu')
                    // Defining attribute 'data-next-item'
                    liMenu.setAttribute('data-next-item', item.next)
                    // Adding menu item to menu container
                    ulMenu.appendChild(liMenu)
                }
            }

        })

        
        // Defining 'VOLTAR AO INÍCIO' item if menu item isn't 'main'
        if (menu.id != 'main'){
            // Defining next menu item of whole menu container
            liMenu = document.createElement('li')
            liMenu.append('VOLTAR')
            // Defining attribute 'data-type-item' as 'menu'
            liMenu.setAttribute('data-type-item', 'menu')
            // Defining attribute 'data-next-item'
            liMenu.setAttribute('data-next-item', menu.previous)
            // Adding menu item to menu container
            ulMenu.appendChild(liMenu)

            // Defining HOME option
            liMenu = document.createElement('li')
            liMenu.append('VOLTAR AO INÍCIO')
            // Defining attribute 'data-type-item' as 'menu'
            liMenu.setAttribute('data-type-item', 'menu')
            // Defining attribute 'data-next-item'
            liMenu.setAttribute('data-next-item', 'main')
            // Adding menu item to menu container
            ulMenu.appendChild(liMenu)
        }



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
                makeMenuItems(homeMenu, user_profile)

                // Defining click event handler on menu container
                menu_container.addEventListener('click', (event) => {
                    const typeItemMenu = event.target.dataset.typeItem
                    
                    if(typeItemMenu === "menu"){
                        event.preventDefault()
                        event.stopPropagation()

                        isRebuilding = true

                        const nextItemMenu = event.target.dataset.nextItem
                        const menuItems = arrayMenu.find(item => item.id === nextItemMenu)

                        if(menuItems){
                            makeMenuItems(menuItems, user_profile)
                            menu_container.classList.add('visible-collum')
                        }
                    }
                })
            })
            .catch(error => {
                console.log("JSON carregou mas menu falhou: " + error)
            })
    }



})