function collapse(id) {
    let x = document.getElementById(id)
    if (x.className.indexOf("w3-show") === -1) {
        x.className += " w3-show"
    } else {
        x.className = x.className.replace(" w3-show", " w3-hide")
    }
}

function sidebar_click() {
    let sidebar = document.getElementsByClassName('w3-sidebar')[0]
    sidebar.style.display === 'none' ? sidebar.style.display = 'block' : sidebar.style.display = 'none'
}