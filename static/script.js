let loginForm = document.getElementById('login');
let signupForm = document.getElementById('signup');
let btn = document.getElementById('btn');

function login() {
    loginForm.style.opacity = "1";
    loginForm.style.pointerEvents = "auto";
    signupForm.style.opacity = "0";
    signupForm.style.pointerEvents = "none";
    btn.style.left = "0px"; // Move button indicator to Login
}

function signup() {
    loginForm.style.opacity = "0";
    loginForm.style.pointerEvents = "none";
    signupForm.style.opacity = "1";
    signupForm.style.pointerEvents = "auto";
    btn.style.left = "110px"; // Move button indicator to Sign Up
}
