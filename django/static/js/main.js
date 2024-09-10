document.getElementById('sms_2fa_active').addEventListener('change', function() {
    var phoneNumberSection = document.getElementById('phone-number-section');
    if (this.checked) {
        phoneNumberSection.style.display = 'block';
    } else {
        phoneNumberSection.style.display = 'none';
    }
});

document.getElementById('email_2fa_active').addEventListener('change', function() {
    var emailSection = document.getElementById('email-section');
    if (this.checked) {
        emailSection.style.display = 'block';
    } else {
        emailSection.style.display = 'none';
    }
});
