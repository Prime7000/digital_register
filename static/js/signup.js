var width = window.screen.availWidth;
var height = window.screen.availHeight;

var form = document.getElementById('signup-prop'); 
console.log("Available Screen Width sighn up ttt:", width);
if (width < 450) {
    form.style.width = '90%';
    // form.style.display = 'none'
}