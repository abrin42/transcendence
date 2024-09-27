from channels.generic.websocket import AsyncWebsocketConsumer
import json
import asyncio
import math
import random

class PongConsumer(AsyncWebsocketConsumer):

                    #        elif type == "updatePts":
                    # await self.sendPts(type, player)

#good
    async def speed_up_ball(self):
        if (self.ball_speed < 10):
            return (0.1)
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
        self.PTSp1 = self.PTSp1 + 1
        await self.send(text_data=json.dumps({
            'type': type,
            'updatePts': self.PTSp1,
            'player': player,
        }))
        self.PTSp2 = self.PTSp2 + 1
        await self.send(text_data=json.dumps({
            'type': type,
            'updatePts': self.PTSp2,
            'player': player,
    }))

    async def sendBall(self, x, y):
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
    async def begin_point(self):
        self.posPad1 = self.boardHeight / 2 - self.paddle_height / 2
        self.posPad2 = self.boardHeight / 2 - self.paddle_height / 2
        self.ball_speed = 2.5
        self.ball_x = self.startXBall
        self.ball_y = self.startYBall
        self.future_x = self.ball_x
        self.future_y = self.ball_y
        await self.sendBall(self.ball_x, self.ball_y)
        # draw_board(left_paddle_current_y, right_paddle_current_y) pour l'instant pas de reste des pad quand point 
        # setTimeout(move_ball, 1500)


#good
    async def  victory(self):
        # await self.sendinfo_back(self.future_x, self.board_x_max, (self.board_x_max / 2))
        if (self.future_x < 0):
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
        while(True):
            # await self.sendPts("updatePts", "1")
            await self.move_ball()
            # self.ball_x = self.ball_x + 1
            await self.sendBall(self.ball_x, self.ball_y)
            await asyncio.sleep(0.01)



    async def connect(self):
        self.PTSp1 = 0
        self.PTSp2 = 0
        self.posPad1 = 280
        self.posPad2 = 280
        self.xPad1 = 10
        self.xPad2 = 700 - 30  # -10 ecart du bord et -20 largeur padel 
        self.paddle_width = 20
        self.paddle_height = 140
        self.position_in_paddle = 0

        self.startXBall = 350
        self.startYBall = 350
        self.ball_x = 350
        self.ball_y = 350
        self.future_x = 350
        self.future_y = 350
        self.ball_angle = 180 if random.random() > 0.5 else 0
        self.ball_speed = 2.5
        self.ball_radius = 7.18

        self.board_y_max = 700
        self.board_x_max = 700
        self.board_min = 3.88

        self.boardWidth = 700
        self.boardHeight = 700

        await self.accept()
        await self.send(text_data=json.dumps({
            'type': 'connection_success',
            'message': 'Connexion réussie!'
        }))
        await asyncio.sleep(1.0)
        asyncio.ensure_future(self.loop_game())
        


    async def disconnect(self, close_code):
        print(f"Déconnexion du client, code: {close_code}")
        if close_code:
            await self.send(text_data=json.dumps({
                'type': 'disconnect',
                'reason': f"Déconnecté avec le code : {close_code}"
            }))
        else:
            await self.send(text_data=json.dumps({
                'type': 'disconnect',
                'reason': 'Déconnexion normale'
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
        if player == 1:
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
            self.posPad2 += 5
            if self.posPad2 > 560:
                self.posPad2 = 560
            newY = self.posPad2
            await self.send(text_data=json.dumps({
                'type': type,
                'newY': newY,
                'player': player,
            }))

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
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({
                'error': 'Format JSON invalide'
            }))