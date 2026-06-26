document.addEventListener('DOMContentLoaded', () =>{

    const btn_rst = document.querySelector('#btn_reset')
    btn_rst.addEventListener('click', function(e){
        e.preventDefault()
        window.location.href = e.currentTarget.dataset.url
    })

    // Getting container with schedule data
    const schedule_data = document.querySelector('#schedule-data')
    
    const str_content = schedule_data.textContent
    let json_content = JSON.parse(str_content)

})