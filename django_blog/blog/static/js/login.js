// Basic login form helper for static check and simple UX.

document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('login-form');
    if (!form) return;

    form.addEventListener('submit', function (e) {
        const username = form.querySelector('input[name="username"]');
        const password = form.querySelector('input[name="password"]');
        if (username && password && (!username.value.trim() || !password.value.trim())) {
            e.preventDefault();
            alert('Please enter both username and password.');
        }
    });
});
