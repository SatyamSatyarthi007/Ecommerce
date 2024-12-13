// Script for navigation bar
function myFunction() {
    var element = document.body;
    element.classList.toggle("dark-mode");
  }
const bar = document.getElementById('bar');
const nav = document.getElementById('navbar');
const close = document.getElementById('close');

if(bar){
  bar.addEventListener('click',() => {
    nav.classList.add('active');
    for (let i = 0; i < nav.children.length; i++) {
      console.log(nav.childNodes[i].childNodes[0]);
      const childLink = nav.childNodes[i].childNodes[0];
      if (!childLink) {
        continue;z
      }
      childLink.classList.add("active");
    }
  })
}

if(close){
  bar.addEventListener('click',() => {
    nav.classList.remove('active');
  })
}

// Login Page
function showLogin() {
  document.getElementById('login-form').style.display = 'block';
  document.getElementById('signup-form').style.display = 'none';
}

function showSignup() {
  document.getElementById('signup-form').style.display = 'block';
  document.getElementById('login-form').style.display = 'none';
}


