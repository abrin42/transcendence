
import { useRouter } from 'vue-router';
import { onMounted } from 'vue';
import { ref, reactive } from 'vue';

export function useUser() {
    const is_connected = ref(false);
    const userAccount = reactive({
        date_joined: "",
        email: "",
        email_2fa_active: "",
        sms_2fa_active: "",
        nickname: "",
        password: "",
        student:"",
        language:"",
        phone_number: "",
        profilePicture: "",
        rank: "",
        username: "",
        lose: "",
        win: "",
        player1Up: "",
        player1Down: "",
        player2Up: "",
        player2Down: "",
        pause: "",
        mute: "",
    });

    const router = useRouter();

    onMounted(async () => {
        await submitForm();
    });

    async function submitForm() {
    try {
        const response = await fetch('api/test-csrf/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include',
        });
        
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        
        const data = await response.json();
        console.log('Response data:', data);
        
    } catch (error) {
        console.error('Error during fetch operation:', error);
    }
}

    function updateUserAccount(user) {
        userAccount.nickname = user.nickname;
        userAccount.username = user.username;
        userAccount.email = user.email;
        userAccount.password = user.password;
        userAccount.phone_number = user.phone_number;
        userAccount.email_2fa_active = user.email_2fa_active;
        userAccount.sms_2fa_active = user.sms_2fa_active;
        userAccount.student = user.student;
        userAccount.language = user.language;
        userAccount.profilePicture = user.profile_picture;
        userAccount.win = user.win;
        userAccount.lose = user.lose;
        userAccount.rank = user.rank;
        // console.log("updateUserAccount.nickname: " + userAccount.nickname);
        // console.log("updateUserAccount.username: " + userAccount.username);
        // console.log("updateUserAccount.email: " + userAccount.email);
        // console.log("updateUserAccount.password: " + userAccount.password);
        // console.log("updateUserAccount.phone_number: " + userAccount.phone_number);
        // console.log("updateUserAccount.email_2fa_active: " + userAccount.email_2fa_active);
        // console.log("updateUserAccount.sms_2fa_active: " + userAccount.sms_2fa_active);
        // console.log("updateUserAccount.student: " + userAccount.student);
        // console.log("updateUserAccount.language: " + userAccount.language);
        //console.log("updateUserAccount.profilePicture: " + userAccount.profilePicture);

        userAccount.player1Up = user.player1Up;
        userAccount.player1Down = user.player1Down;
        userAccount.player2Up = user.player2Up;
        userAccount.player2Down = user.player2Down;
        userAccount.pause = user.pause;
        userAccount.mute = user.mute;

        console.log("updateUserAccount.nickname: " + userAccount.nickname);
        console.log("updateUserAccount.username: " + userAccount.username);
        console.log("updateUserAccount.email: " + userAccount.email);
        console.log("updateUserAccount.password: " + userAccount.password);
        console.log("updateUserAccount.phone_number: " + userAccount.phone_number);
        console.log("updateUserAccount.email_2fa_active: " + userAccount.email_2fa_active);
        console.log("updateUserAccount.sms_2fa_active: " + userAccount.sms_2fa_active);
        console.log("updateUserAccount.student: " + userAccount.student);
        console.log("updateUserAccount.language: " + userAccount.language);
    }

    async function getUser() {
        try {
            const response = await fetch(`api/player/connected_user/`, {
                method: 'GET',
                //credentials: 'include',
            });
    
            if (!response.ok) {
                console.warn(`HTTP error! Status: ${response.status}`);
                const text = await response.text();  // Try to log the raw HTML response
                console.error('Response text:', text);
                is_connected.value = false;
                return;
            }
    
            let user_data;
            try {
                user_data = await response.json();
            } catch (jsonError) {
                console.error('Invalid JSON response:', jsonError);
                is_connected.value = false;
                return;
            }
    
            if (user_data && user_data.is_active) {
                updateUserAccount(user_data);
                is_connected.value = true;
            } else {
                console.log('User is inactive or not found.');
                is_connected.value = false;
            }
        } catch (error) {
            console.error('Error retrieving user data:', error);
            is_connected.value = false;
        }
    }

    return {
        is_connected,
        userAccount,
        getUser,
    };
}
