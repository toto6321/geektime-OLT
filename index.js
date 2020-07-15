function collapse(id) {
    let x = document.getElementById(id)
    if (x.className.indexOf("w3-hide") === -1) {
        x.className += " w3-hide"
    } else {
        x.className = x.className.replace(" w3-hide", "w3-show")
    }
}

function sidebar_click() {
    let sidebar = document.getElementsByClassName('w3-sidebar')[0]
    sidebar.style.display === 'none' ? sidebar.style.display = 'block' : sidebar.style.display = 'none'
}