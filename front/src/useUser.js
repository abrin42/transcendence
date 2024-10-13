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
        phone_number: "",
        profilePicture: "",
        rank: "",
        username: "",
        lose: "",
        win: "",
    });

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
                credentials: 'include',
            });
    
            if (!response.ok) {
                console.warn(`HTTP error! Status: ${response.status}`);
                is_connected.value = false;
                return;
            }
    
            const user = await response.json();
            if (user && !user.error) {
                updateUserAccount(user);
                is_connected.value = true;
    
                //console.log(`getUser/nickname: ${userAccount.value.nickname}`);
                //console.log(`getUser/is_connected: ${is_connected.value}`);
            } else {
                console.log('No user data retrieved.');
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
