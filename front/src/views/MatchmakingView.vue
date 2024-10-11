<script setup>
//imports
    import CreateDropupButton from '../components/CreateDropupButton.vue';
    import CreateBackButton from '../components/CreateBackButton.vue';
    import CreateSoundButton from '../components/CreateSoundButton.vue';
    import { reactive, onMounted, ref } from 'vue';
    import { useRouter } from 'vue-router';

    var myVideo = document.getElementById('videoBG');
    
    myVideo.playbackRate = 2;
    const router = useRouter();

    const userAccount = reactive({
        username:"",
        rank:0,
    });

    
    const waitingPlayer = 1;

    function goToLegacy(id) {
    router.push(`/legacy_remote/${id}`);
}

async function getUser() {
  try {
    const response = await fetch(`api/player/connected_user/`, {
      method: 'GET',
    });
    if (!response.ok) {
      console.warn(`HTTP error! Status: ${response.status}`);
      return;
    }
    const user = await response.json();
    if (user ) {
      userAccount.username = user[0].fields.username;
      userAccount.rank = user[0].fields.rank;
      console.log(userAccount.username)
    } else {
      console.log('No user data retrieved.');
    }
  } catch (error) {
    console.error('Error retrieving user data:', error);
  }
}

async function insertPlayer() {
        
    try {
        const response = await fetch('api/game/insertplayer/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken() // Assuming you have CSRF protection enabled
            },
            body: JSON.stringify({
                username: userAccount.username,
            })
        });
        if (response.ok) {
            const data = await response.json();
            console.log(data);
            if (data.player2 == null)
            {
                await new Promise(resolve => setTimeout(resolve, 1000));
                insertPlayer();
            }
            else
            {
                console.log("lancement dans 3");
                await new Promise(resolve => setTimeout(resolve, 1000));
                console.log("lancement dans 2");
                await new Promise(resolve => setTimeout(resolve, 1000));
                console.log("lancement dans 1");
                await new Promise(resolve => setTimeout(resolve, 1000));
                goToLegacy(data.id);
            }

        }
    } catch (error) {
        console.error('Erreur lors de la connexion:', error);
        alert('An error occurred during login2222');
    }
}

function getCsrfToken() {
    const cookieValue = document.cookie
        .split('; ')
        .find(row => row.startsWith('csrftoken='))
        ?.split('=')[1];
    return cookieValue || '';
}


    onMounted(async () => {
        // await postUser();
        await getUser();
        await insertPlayer();
        console.log(userAccount.id);

    });

    // let waiting = "waiting for opponent";
    // let player1;
    // let player2;
    // const i = 0;

    // //"waiting" text updating with "..."
    // setTimeout(updateText(), 1000);
    // function updateText(){
    //     i += 1;
    //     if (i >= 3)
    //         i = 0;
    //     if(i == 0)
    //         waiting = "waiting for opponent";
    //     if (i == 1)
    //         waiting = "waiting for opponent.";
    //     else if (i == 2)
    //         waiting = "waiting for opponent..";
    //     else if ( i == 3)
    //         waiting = "waiting for opponent...";
    // }

    //when 2nd player is found, we hide "waiting for player" and show opponent
    // if(2nd player found)
    // {
    //     document.getElementbyID('right-side').style.display = show;
    // }
    // else
    // {
    //     document.getElementbyID('right-side').style.display = block;
    //     document.getElementbyID('waiting-text').style.display = show;
    // }
    
</script>

<template>
    <main>
        <img class="profile-picture-matchmaking-left" src="../assets/Chachou.png">
        <img class="profile-picture-matchmaking-right" src="../assets/Chachou.png">
        <div id="wrapper-matchmaking">
            <section class="left">
                <h1 id="game-type">Legacy Pong</h1>
                <h1 class="profile-text-left">{{player1}}</h1>
                <h1 class="profile-text-right">{{player2}}</h1>
                <h1 class="rank-text-left">{{rank1}}</h1>
                <h1 class="rank-text-right">{{rank2}}</h1>
                <h1 class="waiting-text">{{waiting}}</h1>
                <div class="buttonContainer">
                    <div>
                        <CreateSoundButton />
                    </div>
                    <div>
                        <CreateDropupButton />
                    </div>
                    <div>
                        <CreateBackButton />
                    </div>
                </div>
            </section>
            <div class="separation"></div>
            <section id="righ-side" class="right">
                <div>
                    <div class="left-player">
                    </div>
                </div>
            </section>
        </div>
    </main>
</template>

<style lang="scss">
@import './../assets/main.scss';

#wrapper-matchmaking {
    box-shadow: inset 0 0 0 1000px rgba(0,0,0,.2);
}

#game-type{
    position: fixed;
    text-align: center;
    left: 38vw;
    text-align: center;
    font-size: 55px;
    top: 5vh;
    color: white;
}

.profile-picture-matchmaking-left {
    position: fixed;
    width: 250px;
    height: 250px;
    border-radius: 50%;
    top: 30vh;
    left: 20vw;
    border: 5px solid white;
    filter: drop-shadow(5px 5px 4px #0000003b);
}

.profile-text-left {
    position: fixed;
    top: 35vw;
    left: 22vw;
    color: white;
}
.profile-text-right {
    position: fixed;
    top: 35vw;
    right: 22vw;
    color: white;
}

.rank-text-left {
    position: fixed;
    font-size: 25px;
    top: 38vw;
    left: 22vw;
    color: white;
}

.rank-text-right {
    position: fixed;
    font-size: 25px;
    top: 38vw;
    right: 22vw;
    color: white;
}

.waiting-text {
    position: fixed;
    font-size: 25px;
    top: 45vw;
    right: 22vw;
    color: white;
}



.profile-picture-matchmaking-right {
    position: fixed;
    width: 250px;
    height: 250px;
    border-radius: 50%;
    top: 30vh;
    right: 20vw;
    border: 5px solid white;
    filter: drop-shadow(5px 5px 4px #0000003b);
}
</style>