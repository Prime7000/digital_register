var width = window.screen.availWidth;
var card_svg = document.querySelectorAll('.child_icon svg');
var card_icon = document.querySelectorAll('.content');
var child = document.querySelectorAll('.child');
var mainElement = document.querySelector('main');

if (width < 450) {


    if (mainElement) {
        mainElement.style.gap = '0.5rem'; // Use a single gap property
        mainElement.style.justifyContent = 'space-around';
        mainElement.style.padding = '1rem';
    }

    for (var i = 0; i < child.length; i++) {
        child[i].style.width = '40%';
        child[i].style.height = '30%'; // Fixed: removed 'px'
        child[i].style.margin = '0';
        child[i].style.padding = '0';
        child[i].style.textAlign = 'center';
    }



    for (var i = 0; i < card_svg.length; i++) {
        card_svg[i].setAttribute('width', '50');
        card_svg[i].setAttribute('height', '50');
    }
}else{
    for (var i = 0; i < card_svg.length; i++) {
        card_svg[i].setAttribute('width', '50');
        card_svg[i].setAttribute('height', '50');
    }
}