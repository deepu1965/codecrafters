document.addEventListener('DOMContentLoaded', function() {
   
    function fetchUsers() {
        
        fetch('/api/users')
            .then(response => response.json())
            .then(users => {
                console.log('Users:', users);
                // Update the UI with user data
            })
            .catch(error => console.error('Error fetching users:', error));
    }

    function fetchUploads() {
        // Fetch upload data from the backend and update the UI accordingly
        fetch('/api/uploads')
            .then(response => response.json())
            .then(uploads => {
                console.log('Uploads:', uploads);
            })
            .catch(error => console.error('Error fetching uploads:', error));
    }

    fetchUsers();
    fetchUploads();
});
