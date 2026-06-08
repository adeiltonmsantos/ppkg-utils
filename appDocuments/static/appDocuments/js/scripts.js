document.addEventListener('DOMContentLoaded', () =>{

    const btn_rst = document.querySelector('#btn_reset')
    btn_rst.addEventListener('click', function(e){
        e.preventDefault()
        window.location.href = e.currentTarget.dataset.url
    })

    

})