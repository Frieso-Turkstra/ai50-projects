'use strict'

function changeThemeEvent(event) {
    var triggerObject = event.srcElement;

    var body = document.querySelector('body');
    var nav = document.querySelector('nav');
    if (triggerObject.innerHTML == "Light") {
        body.className = "light-theme";
        nav.className = "navbar navbar-expand-lg navbar-light bg-light";
    } else {
        body.className = "dark-theme";
        nav.className = "navbar navbar-expand-lg navbar-dark bg-dark";
    }
};