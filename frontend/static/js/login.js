document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.querySelector('#login-form'); 

    loginForm.addEventListener('submit', function(event) {
        event.preventDefault();

        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;

        // Perform the login request to the Flask backend
        fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `email=${encodeURIComponent(email)}&password=${encodeURIComponent(password)}`,
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Login failed');
            }
            return response.json();
        })
        .then(result => {
            console.log('Login successful:', result);
            // Redirect to the home page or admin dashboard based on user role
            window.location.href = result.isAdmin ? '/admin' : '/';
        })
        .catch(error => {
            console.error('Error logging in:', error);
            // Update the UI to show login failed message
        });
    });
});
