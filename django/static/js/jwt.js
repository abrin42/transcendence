function getCsrfToken() {
    return getCookie('csrftoken');
}

document.addEventListener('DOMContentLoaded', function() {
    const csrfToken = getCsrfToken();    
    //console.log("csrfToken: " + csrfToken)

    if (csrfToken) {
        fetch('/player/verify-jwt/', {
            method: 'POST', // Use POST if that's expected on the server side
            headers: {
                'Authorization': `Bearer ${csrfToken}`,
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken // Include CSRF token in header
            },
            credentials: 'include' // Include cookies in the request
        })
        .then(response => response.json())
        .then(data => {
            console.log('JWT Verification Response:', data);
            if (data.valid) {
                document.getElementById('auth-nav-links').style.display = 'block';
                document.getElementById('guest-nav-links').style.display = 'none';
            } else {
                document.getElementById('auth-nav-links').style.display = 'none';
                document.getElementById('guest-nav-links').style.display = 'block';
            }
        })
        .catch(error => console.error('Error:', error));
    } else {
        document.getElementById('auth-nav-links').style.display = 'none';
        document.getElementById('guest-nav-links').style.display = 'block';
    }
});


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}