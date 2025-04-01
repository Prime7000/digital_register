var width = window.screen.availWidth;
var height = window.screen.availHeight;

var form = document.getElementById('signup-prop'); 
var main  = document.querySelector('main');

console.log("login page");
if (width < 450) {
    form.style.width = '90%';
    main.style.alignItems = 'flex-start';
    main.style.height = 'auto';
    main.style.paddingTop = '30px';

    console.log('working')
}
