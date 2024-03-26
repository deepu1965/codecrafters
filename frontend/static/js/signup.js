document.addEventListener('DOMContentLoaded', function() {
    const signupForm = document.querySelector('#signup-form');

    signupForm.addEventListener('submit', function(event) {
        event.preventDefault();

        const name = document.getElementById('name').value;
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;

        // Perform the signup request to the Flask backend
        fetch('/signup', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            // Encode the form data for sending as POST request body
            body: `name=${encodeURIComponent(name)}&email=${encodeURIComponent(email)}&password=${encodeURIComponent(password)}`,
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Signup failed');
            }
            return response.json();
        })
        .then(result => {
            console.log('Signup successful:', result);
            // Here you can redirect the user to the login page or anywhere you want
            window.location.href = '/login';
        })
        .catch(error => {
            console.error('Error during signup:', error);
            // Update the UI to show a signup failed message
        });
    });
});
