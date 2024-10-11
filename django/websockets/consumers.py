from channels.generic.websocket import AsyncWebsocketConsumer
import json
import asyncio
import math
import random
from datetime import datetime
import urllib.parse
from . import remote 

lstgame = []

connected_websockets = []
class PongConsumer(AsyncWebsocketConsumer):
    players = set()
                    #        elif type == "updatePts":
                    # await self.sendPts(type, player)

#good
    async def speed_up_ball(self):
        if (self.ball_speed < 10):
            return (0.2)
        return (0)

#good
    async def paddle_collisions(self):
        if (self.future_x <= self.xPad1  + self.paddle_width + self.ball_radius and self.future_x >= self.xPad1  and self.future_y >= self.posPad1 - self.ball_radius and self.future_y <= self.posPad1 + self.paddle_height + self.ball_radius):
            self.position_in_paddle = (2 * (self.ball_y + self.ball_radius - self.posPad1) / (self.paddle_height + self.ball_radius * 2)) - 1
            self.ball_angle = 80 * self.position_in_paddle
            self.ball_x += self.ball_radius / 10
            self.ball_speed += await self.speed_up_ball()

        if (self.future_x >= self.xPad2 - self.ball_radius and self.future_x <= self.xPad2 + self.ball_radius / 2 and self.future_y >= self.posPad2 - self.ball_radius and self.future_y <= self.posPad2 + self.paddle_height + self.ball_radius):
            self.position_in_paddle = (2 * (self.ball_y + self.ball_radius - self.posPad2) / (self.paddle_height + self.ball_radius * 2)) - 1
            self.ball_angle = 180 - 80 * self.position_in_paddle
            self.ball_x -= self.ball_radius / 10
            self.ball_speed += await self.speed_up_ball()



    async def sendPts(self, type, player):
        if player == "1":
            self.PTSp1 = self.PTSp1 + 1
            await self.send(text_data=json.dumps({
                'type': type,
                'updatePts': self.PTSp1,
                'player': player,
            }))
            if (self.PTSp1 == self.nb_pts_for_win):
                await self.endGame()

        elif player == "2":
            self.PTSp2 = self.PTSp2 + 1
            await self.send(text_data=json.dumps({
                'type': type,
                'updatePts': self.PTSp2,
                'player': player,
            }))
            if (self.PTSp2 == self.nb_pts_for_win):
                await self.endGame()
            

    async def sendBall(self, x, y):
        if self.is_online == 0:
            await self.send(text_data=json.dumps({
                'type': "updateBaal",
                'x': x,
                'y': y,
            }))


    async def sendinfo_back(self, value_back1, value_back2 ,value_back3):
        await self.send(text_data=json.dumps({
            'type': "info_back",
            'value_back1': value_back1,
            'value_back2': value_back2,
            'value_back3': value_back3,
        }))

#good


    async def endGame(self):
        self.Game_on = -1
        await self.disconnect(1000)
        await self.send(text_data=json.dumps({
            'type': "endGame",
        }))


    async def sendPadInit(self):
        await self.send(text_data=json.dumps({
            'type': "mouvUp",
            'newY': self.init_pad,
            'player': "1",
        }))
        await self.send(text_data=json.dumps({
            'type': "mouvUp",
            'newY': self.init_pad,
            'player': "2",
        }))

    async def begin_point(self):
        self.posPad1 = self.init_pad
        self.posPad2 = self.init_pad
        self.ball_speed = self.init_ball_speed 
        self.ball_x = self.startXBall
        self.ball_y = self.startYBall
        self.future_x = self.ball_x
        self.future_y = self.ball_y
        await self.sendBall(self.ball_x, self.ball_y)
        await self.sendPadInit()
        self.ball_future_position = self.init_pad
        self.time_to_get_future_position = 1
        await asyncio.sleep(1)
        #         self.posPad1 = 280
        # self.posPad2 = 280
        # draw_board(left_paddle_current_y, right_paddle_current_y) pour l'instant pas de reste des pad quand point 
        # setTimeout(move_ball, 1500)


#good
    async def  victory(self):
        # await self.sendinfo_back(self.future_x, 0, 0)
        if (self.future_x < 6.983):
            await self.sendPts("updatePts", "2")
            self.ball_angle = 180
            await self.begin_point()
        else:
            await self.sendPts("updatePts", "1")
            self.ball_angle = 0
            await self.begin_point()


#good
    async def wall_collisions(self):
        # await self.sendinfo_back(self.future_x + self.ball_radius, self.board_x_max, 85600)
        if (self.future_x < self.board_min + self.ball_radius or self.future_x + self.ball_radius > self.board_x_max):
            await self.victory()
            return (1)
        if (self.future_y < self.board_min + self.ball_radius):
            self.future_y = self.board_min + self.ball_radius
            self.ball_angle *= -1
            # self.ball_angle = -self.ball_angle
        if (self.future_y > self.board_y_max - self.ball_radius):
            self.future_y = self.board_y_max - self.ball_radius
            self.ball_angle *= -1
            # self.ball_angle = -self.ball_angle
        self.ball_x = self.future_x
        self.ball_y = self.future_y
        return (0)


    async def move_ball(self):
        self.future_x = self.ball_x + math.cos(self.ball_angle * math.pi / 180) * self.ball_speed * (self.boardWidth + self.boardHeight) / 2000
        self.future_y = self.ball_y + math.sin(self.ball_angle * math.pi / 180) * self.ball_speed * (self.boardWidth + self.boardHeight) / 2000
        # self.future_x += 3
        if await self.wall_collisions() == 0:
            await self.paddle_collisions()

        
        
        # self.ball_x = self.ball_x + 1
        # await self.sendBall(self.ball_x, self.ball_y)
            # draw_board(self.posPad1, self.posPad2)
            # setTimeout(move_ball, 1)
            # await asyncio.sleep(1.0)


    async def loop_game(self):
        while self.Game_on != -1:
            while(self.Game_on == 1):
                # await self.sendPts("updatePts", "1")
                await self.move_ball()
                # self.ball_x = self.ball_x + 1
                await self.sendBall(self.ball_x, self.ball_y)
                await asyncio.sleep(self.tick_back)
            await asyncio.sleep(0.5)

    async def ai_get_future_position(self):
        if (self.ball_last_direction == 1 and self.time_to_get_future_position == True):
            self.time_to_get_future_position = False
            
            velocity_x = math.cos(self.ball_angle * math.pi / 180) * self.ball_speed * (self.boardWidth + self.boardHeight) / 2000
            velocity_y = math.sin(self.ball_angle * math.pi / 180) * self.ball_speed * (self.boardWidth + self.boardHeight) / 2000
            self.ball_future_position = (self.xPad2 - self.ball_x - self.ball_radius * 2) / velocity_x * velocity_y + self.ball_y
            while (self.ball_future_position < self.board_min or self.ball_future_position > self.boardHeight):
                if (self.ball_future_position < self.board_min):
                    self.ball_future_position *= -1
                if (self.ball_future_position > self.boardHeight):
                    self.ball_future_position = self.boardHeight - self.ball_future_position % self.boardHeight
            rebound_count = int(self.ball_future_position / self.boardHeight)
            await self.sendinfo_back("velocity_x ; y",velocity_x,velocity_y)
            await self.sendinfo_back("--------------------------------------------",0,0)
            await self.sendinfo_back("rebound",rebound_count,self.ball_future_position)

    async def ai_get_infos_every_second(self):
        self.current_time = datetime.now().timestamp()
        # await self.sendinfo_back("current / begin",self.current_time % 10, self.begin_time % 10)
        if (self.current_time - self.begin_time >= 1):
            self.begin_time = datetime.now().timestamp()
            self.ball_last_position = self.ball_y
            await self.ai_get_future_position()
            if (self.ball_last_direction == 1 and (self.ball_angle > 90 or self.ball_angle < -90)):
                self.begin_time = datetime.now().timestamp()
                await self.sendinfo_back("begin time reinitialized",self.begin_time, 0)
            self.ball_last_angle = self.ball_angle
            if (self.ball_last_angle > 90 or self.ball_last_angle < -90):
                self.ball_last_direction = -1
                self.time_to_get_future_position = True
            else:
                self.ball_last_direction = 1

            self.random_paddle_pos = random.random() * 1000 % self.paddle_height
            # await self.sendinfo_back("random_paddle_pos",self.random_paddle_pos, 0)

    async def ai_back_to_center(self):
        if (self.ball_last_direction == -1):
            self.ball_future_position  = self.boardHeight / 2
            if (self.posPad2 < self.init_pad - 5):
                await self.sendPadDown("mouvDown", 2)
            elif (self.posPad2 > self.init_pad + 5):
                await self.sendPadUp("mouvUp", 2)

    async def ai_catch_ball(self):
        if (self.ball_last_direction == 1):
            # if (self.ball_future_position < self.posPad2 + self.random_paddle_pos - 5):
            if (self.ball_future_position < self.posPad2 + self.paddle_height / 2):
                await self.sendPadUp("mouvUp", 2)
            # elif (self.ball_future_position > self.posPad2 + self.random_paddle_pos + 5):
            elif (self.ball_future_position > self.posPad2 + self.paddle_height / 2):
                await self.sendPadDown("mouvDown", 2)
        # if (self.ball_last_angle <= 0 and self.ball_last_angle > -90):
        #     await self.sendinfo_back("detect ball haut",self.ball_future_position, self.posPad2)
        #     # if (self.ball_future_position < self.posPad2 + self.random_paddle_pos):
        #     if (self.ball_future_position < self.posPad2):
        #         await self.sendPadUp("mouvUp", 2)
        #     else:
        #         await self.sendPadDown("mouvDown", 2)
        # if (self.ball_last_angle >= 0 and self.ball_last_angle < 90):
        #     await self.sendinfo_back("detect ball bas",self.ball_future_position, self.posPad2)
        #     # if (self.ball_future_position > self.posPad2 + self.random_paddle_pos):
        #     if (self.ball_future_position > self.posPad2):
        #         await self.sendPadDown("mouvDown", 2)
        #     else:
        #         await self.sendPadUp("mouvUp", 2)

    async def ai_loop_game(self):
        while self.P1Ready == 0:
            await asyncio.sleep(0.5)
        self.begin_time = datetime.now().timestamp()
        while True and self.P1Ready == 1:
            await self.ai_get_infos_every_second()
            await self.ai_back_to_center()
            await self.ai_catch_ball()
            await asyncio.sleep(self.tick_back)

    async def initForLocal(self):
        self.boardWidth = 700
        self.boardHeight = 700
        self.AI = 0

        self.init_ball_speed = 4
        self.tick_back = 0.01

        self.Game_on = 0
        self.nb_pts_for_win = 10

        self.P1Ready = 0
        self.P2Ready = 0

        self.PTSp1 = 0
        self.PTSp2 = 0
        self.xPad1 = 10
        self.xPad2 = 700 - 30  # -10 ecart du bord et -20 largeur padel 
        self.paddle_width = 20
        self.paddle_height = 140
        self.position_in_paddle = 0
        self.init_pad = self.boardHeight / 2 - self.paddle_height / 2
        self.posPad1 = self.init_pad
        self.posPad2 = self.init_pad

        self.startXBall = 350
        self.startYBall = 350
        self.ball_x = 350
        self.ball_y = 350
        self.future_x = 350
        self.future_y = 350
        self.ball_angle = 180 if random.random() > 0.5 else 0
        self.ball_radius = 7.18
        self.ball_speed = self.init_ball_speed

        self.board_y_max = 700
        self.board_x_max = 700
        # self.board_min = 3.88
        self.board_min = 0
        self.is_online = 0

        # ⊱━━━.⋅εïз⋅.━━━⊰   AI   ⊱━━━.⋅εïз⋅.━━━⊰ #
        self.begin_time = datetime.now().timestamp()
        self.current_time = datetime.now().timestamp()
        self.ball_last_position = self.ball_y
        self.ball_last_angle = self.ball_angle
        self.random_paddle_pos = random.random() * 1000 % self.paddle_height
        self.ball_future_position = self.ball_x
        self.ball_last_direction = -1 if self.ball_angle == 180 else 1
        self.time_to_get_future_position = True
        asyncio.ensure_future(self.loop_game())



    async def create_new_game(self, game_id):
        return {
            "gameID": game_id,
            "wsj1": self,
            "wsj2": 0,
            "boardWidth": 700,
            "boardHeight": 700,
            "AI": 0,
            "init_ball_speed": 4,
            "tick_back": 0.01,
            "Game_on": 0,
            "nb_pts_for_win": 10,
            "P1Ready": 0,
            "P2Ready": 0,
            "PTSp1": 0,
            "PTSp2": 0,
            "xPad1": 10,
            "xPad2": 700 - 30,  # -10 écart du bord et -20 largeur padel 
            "paddle_width": 20,
            "paddle_height": 140,
            "position_in_paddle": 0,
            "init_pad": 700 / 2 - 140 / 2,
            "posPad1": 700 / 2 - 140 / 2,
            "posPad2": 700 / 2 - 140 / 2,
            "startXBall": 350,
            "startYBall": 350,
            "ball_x": 350,
            "ball_y": 350,
            "future_x": 350,
            "future_y": 350,
            "ball_angle": 180 if random.random() > 0.5 else 0,
            "ball_radius": 7.18,
            "ball_speed": 4,
            "board_y_max": 700,
            "board_x_max": 700,
            "board_min": 0,
            "is_online": 1,
            # "thread_online": 0,
        }
















# ==========================================================================================================================
# ==========================================================================================================================
#                                                 remote
# ==========================================================================================================================
# ==========================================================================================================================


    async def speed_up_ball_remote(game):
        if (game.ball_speed < 10):
            return (0.2)
        return (0)

    async def paddle_collisions_remote(game):
        if (game.future_x <= game.xPad1  + game.paddle_width + game.ball_radius and game.future_x >= game.xPad1  and game.future_y >= game.posPad1 - game.ball_radius and game.future_y <= game.posPad1 + game.paddle_height + game.ball_radius):
            game.position_in_paddle = (2 * (game.ball_y + game.ball_radius - game.posPad1) / (game.paddle_height + game.ball_radius * 2)) - 1
            game.ball_angle = 80 * game.position_in_paddle
            game.ball_x += game.ball_radius / 10
            game.ball_speed += await game.speed_up_ball_remote()

        if (game.future_x >= game.xPad2 - game.ball_radius and game.future_x <= game.xPad2 + game.ball_radius / 2 and game.future_y >= game.posPad2 - game.ball_radius and game.future_y <= game.posPad2 + game.paddle_height + game.ball_radius):
            game.position_in_paddle = (2 * (game.ball_y + game.ball_radius - game.posPad2) / (game.paddle_height + game.ball_radius * 2)) - 1
            game.ball_angle = 180 - 80 * game.position_in_paddle
            game.ball_x -= game.ball_radius / 10
            game.ball_speed += await game.speed_up_ball_remote()


    async def endGame_remote(game):
        game.Game_on = -1
        await game.disconnect(1000)
        await game.send(text_data=json.dumps({
            'type': "endGame",
        }))


    async def sendPts_remote(game, type, player):
        if player == "1":
            game.PTSp1 = game.PTSp1 + 1
            await game.send(text_data=json.dumps({
                'type': type,
                'updatePts': game.PTSp1,
                'player': player,
            }))
            if (game.PTSp1 == game.nb_pts_for_win):
                await game.endGame_remote()

        elif player == "2":
            game.PTSp2 = game.PTSp2 + 1
            await game.send(text_data=json.dumps({
                'type': type,
                'updatePts': game.PTSp2,
                'player': player,
            }))
            if (game.PTSp2 == game.nb_pts_for_win):
                await game.endGame_remote()



    async def sendPadInit_remote(game):
        await game.send(text_data=json.dumps({
            'type': "mouvUp",
            'newY': game.init_pad,
            'player': "1",
        }))
        await game.send(text_data=json.dumps({
            'type': "mouvUp",
            'newY': game.init_pad,
            'player': "2",
        }))

    async def begin_point_remote(game):
        game.posPad1 = game.init_pad
        game.posPad2 = game.init_pad
        game.ball_speed = game.init_ball_speed 
        game.ball_x = game.startXBall
        game.ball_y = game.startYBall
        game.future_x = game.ball_x
        game.future_y = game.ball_y
        await game.sendBall_remote(game.ball_x, game.ball_y)
        await game.sendPadInit_remote()
        game.ball_future_position = game.init_pad
        game.time_to_get_future_position = 1
        await asyncio.sleep(1)
#good
    async def  victory_remote(game):
        # await self.sendinfo_back(self.future_x, 0, 0)
        if (game.future_x < 6.983):
            await game.sendPts_remote("updatePts", "2")
            game.ball_angle = 180
            await game.begin_point_remote()
        else:
            await game.sendPts_remote("updatePts", "1")
            game.ball_angle = 0
            await game.begin_point_remote()

#good
    async def wall_collisions_remote(game):
        # await self.sendinfo_back(self.future_x + self.ball_radius, self.board_x_max, 85600)
        if (game.future_x < game.board_min + game.ball_radius or game.future_x + game.ball_radius > game.board_x_max):
            await game.victory_remote()
            return (1)
        if (game.future_y < game.board_min + game.ball_radius):
            game.future_y = game.board_min + game.ball_radius
            game.ball_angle *= -1
            # game.ball_angle = -game.ball_angle
        if (game.future_y > game.board_y_max - game.ball_radius):
            game.future_y = game.board_y_max - game.ball_radius
            game.ball_angle *= -1
            # game.ball_angle = -game.ball_angle
        game.ball_x = game.future_x
        game.ball_y = game.future_y
        return (0)

#good
    async def move_ball_remote(game):
        game.future_x = game.ball_x + math.cos(game.ball_angle * math.pi / 180) * game.ball_speed * (game.boardWidth + game.boardHeight) / 2000
        game.future_y = game.ball_y + math.sin(game.ball_angle * math.pi / 180) * game.ball_speed * (game.boardWidth + game.boardHeight) / 2000
        # game.future_x += 3
        if await game.wall_collisions_remote() == 0:
            await game.paddle_collisions_remote()

# wsj1
# wsj2

    async def sendBall_remote(game, x, y):
        if game.is_online == 0:
            await game.wsj1.send(text_data=json.dumps({
                'type': "updateBaal",
                'x': x,
                'y': y,
            }))
            await game.wsj2.send(text_data=json.dumps({
                'type': "updateBaal",
                'x': x,
                'y': y,
            }))

#good
    async def loop_game_remote(game):
        while True:
            game.ball_x = game.ball_x + 6
            await game.sendBall_remote()
            await asyncio.sleep(0.5)

        # while game.Game_on != -1:
        #     while(game.Game_on == 1):
        #         # await game.sendPts("updatePts", "1")
        #         await game.move_ball_remote()
        #         # game.ball_x = game.ball_x + 1
        #         await game.sendBall_remote(game.ball_x, game.ball_y)
        #         await asyncio.sleep(game.tick_back)
        #     await asyncio.sleep(0.5)



    async def initRemote(self, id):
        if not any(game['gameID'] == id for game in lstgame): #creat la game si pas cree
            new_game = self.create_new_game(id)
            lstgame.append(new_game)
            print("new game is set")

        else:
            print("else for seconde player")
            for game in lstgame:
                if game['gameID'] == id:
                    game['wsj2'] = self
                    game.is_online = 0
                    print("go to thread")
                    asyncio.ensure_future(self.loop_game_remote())

        



    async def connect(self):
        print("principale conect")
        query_string = self.scope['query_string'].decode('utf-8')
        query_params = urllib.parse.parse_qs(query_string)        
        page_url = query_params.get('page', [''])[0]
        page_url.replace("game_", "")
        if (page_url == "legacy" or page_url == "ia"):
            await self.initForLocal()
        elif(page_url.isdigit()):
            print("is a remote game")
            await self.initRemote(page_url)





        # print(f"Le WebSocket est créé sur la page : {page_url}")
        # if (current_path == "I")
            
        connected_websockets.append(self)
        await self.accept()
        await self.send(text_data=json.dumps({
            'type': 'connection_success',
            'message': 'Connexion réussie!'
        }))
        


    async def disconnect(self, close_code):
        if (close_code == 1000):     #fin de partie normal
                if self in connected_websockets:
                    connected_websockets.remove(self) 
                await self.send(text_data=json.dumps({
                'type': 'disconnect',
                'close_code': close_code
            }))
        elif (close_code == 1001): #joueur qui part de la partie donc mettre en pause
            self.Game_on = 0
            await self.send(text_data=json.dumps({
                'type': 'disconnect',
                'close_code': close_code

            }))

# player1 = joueur de gauche 
# player2 = joueur de droite 

    
    # async def stopSendUp(self, player):
    #     if player == 1:
    #         self.mouvUp1 = 0
    #         await self.send(text_data=json.dumps({ 
    #                 'type': "info_back",
    #                 'print_back': "Arrêt du mouvement du joueur 1",
    #                 'value_back': self.mouvUp1,
                    
    #             })) #a enlever test
    #         # await asyncio.sleep(0.01)

    async def sendPadUp(self, type, player):
        if player == 1:
            self.P1Ready = 1
            self.posPad1 -= 5
            if self.posPad1 < 0:
                self.posPad1 = 0
            newY = self.posPad1
            await self.send(text_data=json.dumps({
                'type': type,
                'newY': newY,
                'player': player,
            }))
        if player == 2:
            self.P2Ready = 1
            self.posPad2 -= 5
            if self.posPad2 < 0:
                self.posPad2 = 0
            newY = self.posPad2
            await self.send(text_data=json.dumps({
                'type': type,
                'newY': newY,
                'player': player,
            }))

    async def sendPadDown(self, type, player):
        # await self.sendinfo_back("hereeeee",type, player)
        if player == 1:
            self.P1Ready = 1
            self.posPad1 += 5
            if self.posPad1 > 560:
                self.posPad1 = 560
            newY = self.posPad1
            await self.send(text_data=json.dumps({
                'type': type,
                'newY': newY,
                'player': player,
            }))
        if player == 2:
            # await self.sendinfo_back("je passe dans 2 laaa", type ,player)
            self.P2Ready = 1
            self.posPad2 += 5
            if self.posPad2 > 560:
                self.posPad2 = 560
            newY = self.posPad2
            await self.send(text_data=json.dumps({
                'type': type,
                'newY': newY,
                'player': player,
            }))

    async def sendStart(self):
        await self.send(text_data=json.dumps({
            'type': "startGame",
        }))
        # await asyncio.sleep(3.0)
        # self.posPad1 = self.init_pad
        # self.posPad2 = self.init_pad
        # await self.sendPadInit()
        self.Game_on = 1

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            
            type = data.get('type')
            player = int(data.get('player', 0))

            if type and player:
                if type == "mouvUp":
                    await self.sendPadUp(type, player)
                elif type == "mouvDown":
                    await self.sendPadDown(type, player)
                elif type == "GameIA":
                    self.AI = 1
                    self.P2Ready = 1
                    asyncio.ensure_future(self.ai_loop_game())

            if self.P1Ready == 1 and self.P2Ready == 1 and self.Game_on == 0:
                await self.sendStart()

        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({
                'error': 'Format JSON invalide'
            }))
