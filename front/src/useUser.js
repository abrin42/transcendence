import { ref, reactive } from 'vue';

export function useUser() {
    const is_connected = ref(false);
    const userAccount = reactive({
        username: "",
        nickname: "",
        phone_number: "",
        email: "",
        password: "",
        newpassword: "",
        email_2fa_active: "",
        sms_2fa_active: "",
        profilePicture: "",
        student:"",
        language:"",
        date_joined: "",
        rank: "",
        lose: "",
        win: "",
        player1Up: "KeyW",
        player1Down: "KeyS",
        player2Up: "ArrowUp",
        player2Down: "ArrowDown",
        pause: "KeyP",
        mute: "KeyM",
        anonymized: "",
    });

    function updateUserAccount(user) {
        userAccount.nickname = user.nickname;
        userAccount.username = user.username;
        userAccount.email = user.email;
        userAccount.password = user.password;
        userAccount.newpassword = user.newpassword;
        userAccount.phone_number = user.phone_number;
        userAccount.email_2fa_active = user.email_2fa_active;
        userAccount.sms_2fa_active = user.sms_2fa_active;
        userAccount.student = user.student;
        userAccount.language = user.language;
        userAccount.profilePicture = user.profile_picture;
        userAccount.anonymized = user.anonymized;
        userAccount.date_joined = user.date_joined;
        
        userAccount.win = user.win;
        userAccount.lose = user.lose;
        userAccount.rank = user.rank;

        userAccount.player1Up = user.player1Up;
        userAccount.player1Down = user.player1Down;
        userAccount.player2Up = user.player2Up;
        userAccount.player2Down = user.player2Down;
        userAccount.pause = user.pause;
        userAccount.mute = user.mute;
    }

    async function getUser() {
        try {
            const response = await fetch(`/api/player/connected_user/`, {
                method: 'GET',
                credentials: 'include',
                headers: {
                    'Cache-Control': 'private',
                },
            });
            if (response.status == 204) {
                is_connected.value = false;
                return;
            }
            const user = await response.json();
            if (user && !user.error) {
                updateUserAccount(user);
                is_connected.value = true;
            } else {
                console.log('No user data retrieved.');
                is_connected.value = false;
            }
        } catch (error) {
            console.error('Error retrieving user data /useUser:', error);
            is_connected.value = false;
        }
    }

    return {
        is_connected,
        userAccount,
        getUser,
    };
}