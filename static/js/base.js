const width = window.screen.availWidth;
const height = window.screen.availHeight;
console.log("Available Screen Width:", width);
console.log("Available Screen Height:", height);
console.log('prime')
console.log(typeof width)


var sidebar = document.querySelector('.container > div:nth-child(1)');
var content = document.querySelector('.container > div:nth-child(2)');
var menu = document.getElementById('menu')
var icon = document.getElementById('menu-icon');
// the part that welcomes user
document.getElementById('result').innerText = 'welcome Prime';

// the part that gives menu action
icon.addEventListener('click', () => {
    if (sidebar.style.display === 'none') {
        sidebar.style.display = 'block';
    } else {
        sidebar.style.display = 'none';
    }
})



if (width < 450) {
    // sidebar.style.flexBasis  = '0%';
    sidebar.style.display = 'none';
    // content.style.flexBasis = '100%';
    content.style.width = '100%';
    content.style.padding = '3px';
    menu.style.justifyContent = 'space-between'
    console.log('width < 451')
    content.style.flexBasis = '100%';
}else{
    document.getElementById('menu-icon').style.display = 'none';
    menu.style.justifyContent = 'flex-end'
    menu.style.paddingRight = '7px'
}