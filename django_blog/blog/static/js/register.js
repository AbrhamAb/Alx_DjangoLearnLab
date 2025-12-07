// Basic registration form helper for static check and simple UX.

document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('register-form');
    if (!form) return;

    form.addEventListener('submit', function (e) {
        const password1 = form.querySelector('input[name*="password1"]');
        const password2 = form.querySelector('input[name*="password2"]');
        if (password1 && password2 && password1.value !== password2.value) {
            e.preventDefault();
            alert('Passwords do not match.');
        }
    });
});
