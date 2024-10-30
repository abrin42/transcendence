from channels.generic.websocket import AsyncWebsocketConsumer
import json
import asyncio
import math
import random
from datetime import datetime
import urllib.parse
import time

lstgame = {}


class PongConsumer(AsyncWebsocketConsumer):


# ==========================================================================================================================
# ==========================================================================================================================
#                                                 ia
# ==========================================================================================================================
# ==========================================================================================================================


    async def ai_get_future_position(self):
        if (self.ball_last_direction == 1):
            velocity_x = math.cos(self.ball_angle * math.pi / 180) * self.ball_speed * (self.boardWidth + self.boardHeight) / 2000
            velocity_y = math.sin(self.ball_angle * math.pi / 180) * self.ball_speed * (self.boardWidth + self.boardHeight) / 2000
            self.ball_future_position = (self.xPad2 - self.ball_x - self.ball_radius * 2) / velocity_x * velocity_y + self.ball_y
            while (self.ball_future_position < self.board_min or self.ball_future_position > self.boardHeight):
                if (self.ball_future_position < self.board_min):
                    self.ball_future_position *= -1
                if (self.ball_future_position > self.boardHeight):
                    self.ball_future_position = self.boardHeight - self.ball_future_position % self.boardHeight

    async def ai_get_infos_every_second(self):
        self.current_time = datetime.now().timestamp()
        if (self.current_time - self.begin_time >= 1):
            self.begin_time = datetime.now().timestamp()
            if (self.ball_angle > 90 or self.ball_angle < -90):
                self.ball_last_direction = -1
            else:
                self.ball_last_direction = 1
            await self.ai_get_future_position()
            self.random_paddle_pos = random.random() * 1000 % self.paddle_height

    async def ai_back_to_center(self):
        if (self.ball_last_direction == -1):
            if (self.posPad2 < self.init_pad - 5):
                await self.sendPadDown(2)
            elif (self.posPad2 > self.init_pad + 5):
                await self.sendPadUp(2)

    async def ai_catch_ball(self):
        if (self.ball_last_direction == 1):
            if (self.ball_future_position < self.posPad2 + self.random_paddle_pos - 5):
                await self.sendPadUp(2)
            elif (self.ball_future_position > self.posPad2 + self.random_paddle_pos + 5):
                await self.sendPadDown(2)

    async def ai_loop_game(self):
        while self.P1Ready == 0:
            await asyncio.sleep(0.5)
        self.begin_time = datetime.now().timestamp()
        while True and self.P1Ready == 1:
            await self.ai_get_infos_every_second()
            await self.ai_back_to_center()
            await self.ai_catch_ball()
            await asyncio.sleep(self.tick_back)


# ==========================================================================================================================
# ==========================================================================================================================
#                                                   remote 
# ==========================================================================================================================
# ==========================================================================================================================



    # async def sendpaddleHit(self):
    #     await self.channel_layer.group_send(
    #         self.room_group_name,
    #         {
    #             'type': 'paddle_Hit',
    #         }
    #     )
    
    # async def paddle_Hit(self, event):
    #     await self.send(text_data=json.dumps({
    #         'type': 'paddleHit',
    #     }))


    async def paddleHitRemote(self):
        await self.channel_layer.group_send(
            self.room_id,
            {
                'type': 'paddle_HitRemote',
            }
        )
    
    async def paddle_HitRemote(self, event):
        await self.send(text_data=json.dumps({
            'type': 'paddleHit',
        }))



    async def speed_up_ball_remote(self):
        if (lstgame[self.room_id]['ball_speed'] < 10):
            return (0.2)
        return (0)

    async def paddle_collisions_remote(self):
        if (lstgame[self.room_id]['future_x'] <= lstgame[self.room_id]['xPad1']  + lstgame[self.room_id]['paddle_width'] + lstgame[self.room_id]['ball_radius'] and lstgame[self.room_id]['future_x'] >= lstgame[self.room_id]['xPad1']  and lstgame[self.room_id]['future_y'] >= lstgame[self.room_id]['posPad1'] - lstgame[self.room_id]['ball_radius'] and lstgame[self.room_id]['future_y'] <= lstgame[self.room_id]['posPad1'] + lstgame[self.room_id]['paddle_height'] + lstgame[self.room_id]['ball_radius']):
            lstgame[self.room_id]['position_in_paddle'] = (2 * (lstgame[self.room_id]['ball_y'] + lstgame[self.room_id]['ball_radius'] - lstgame[self.room_id]['posPad1']) / (lstgame[self.room_id]['paddle_height'] + lstgame[self.room_id]['ball_radius'] * 2)) - 1
            lstgame[self.room_id]['ball_angle'] = 80 * lstgame[self.room_id]['position_in_paddle']
            lstgame[self.room_id]['ball_x'] += lstgame[self.room_id]['ball_radius'] / 10
            lstgame[self.room_id]['ball_speed'] += await self.speed_up_ball_remote()
            await self.paddleHitRemote()


        if (lstgame[self.room_id]['future_x'] >= lstgame[self.room_id]['xPad2'] - lstgame[self.room_id]['ball_radius'] and lstgame[self.room_id]['future_x'] <= lstgame[self.room_id]['xPad2'] + lstgame[self.room_id]['ball_radius'] / 2 and lstgame[self.room_id]['future_y'] >= lstgame[self.room_id]['posPad2'] - lstgame[self.room_id]['ball_radius'] and lstgame[self.room_id]['future_y'] <= lstgame[self.room_id]['posPad2'] + lstgame[self.room_id]['paddle_height'] + lstgame[self.room_id]['ball_radius']):
            lstgame[self.room_id]['position_in_paddle'] = (2 * (lstgame[self.room_id]['ball_y'] + lstgame[self.room_id]['ball_radius'] - lstgame[self.room_id]['posPad2']) / (lstgame[self.room_id]['paddle_height'] + lstgame[self.room_id]['ball_radius'] * 2)) - 1
            lstgame[self.room_id]['ball_angle'] = 180 - 80 * lstgame[self.room_id]['position_in_paddle']
            lstgame[self.room_id]['ball_x'] -= lstgame[self.room_id]['ball_radius'] / 10
            lstgame[self.room_id]['ball_speed'] += await self.speed_up_ball_remote()
            await self.paddleHitRemote()


    async def endGame_remote(self):
        lstgame[self.room_id]['Game_on']= -1
        await self.channel_layer.group_send(
            self.room_id,
            {
                'type': 'gameEnded',
            }
        )

    async def gameEnded(self, event):
        await self.send(text_data=json.dumps({
            'type': 'endGame',
        }))
        await self.disconnect(1000)


    async def sendPts_remote(self, type, player):
        if player == "1":
            lstgame[self.room_id]['PTSp1'] += 1
            updatePts = lstgame[self.room_id]['PTSp1']
        elif player == "2":
            lstgame[self.room_id]['PTSp2'] += 1
            updatePts = lstgame[self.room_id]['PTSp2']
        else:
            updatePts = lstgame[self.room_id]['PTSp1']
            await self.channel_layer.group_send(
                self.room_id,
                {
                    'type': 'updatePts',
                    'updatePts': updatePts,
                    'player': "-1",
                }
            )
            player = "-2"
            updatePts = lstgame[self.room_id]['PTSp2']

        await self.channel_layer.group_send(
            self.room_id,
            {
                'type': 'updatePts',
                'updatePts': updatePts,
                'player': player,
            }
        )

        if (lstgame[self.room_id]['PTSp1'] == lstgame[self.room_id]['nb_pts_for_win']) or \
            lstgame[self.room_id]['PTSp2'] == lstgame[self.room_id]['nb_pts_for_win']:
            await self.endGame_remote()

    async def updatePts(self, event):
        await self.send(text_data=json.dumps({
            'type': event['type'],
            'updatePts': event['updatePts'],
            'player': event['player'],
        }))

    async def sendPadInit_remote(self):
        await self.channel_layer.group_send(
            self.room_id,
            {
                'type': 'update_paddle_position',
                'newY': lstgame[self.room_id]['init_pad'],
                'player': "1",
            }
        )
        await self.channel_layer.group_send(
            self.room_id,
            {
                'type': 'update_paddle_position',
                'newY': lstgame[self.room_id]['init_pad'], 
                'player': "2",
            }
        )

    async def update_paddle_position(self, event):
        newY = event['newY']
        player = event['player']
        await self.send(text_data=json.dumps({
            'type': 'updatePaddle',
            'newY': newY,
            'player': player,
        }))

    async def begin_point_remote(self):
        lstgame[self.room_id]['posPad1'] = lstgame[self.room_id]['init_pad']
        lstgame[self.room_id]['posPad2'] = lstgame[self.room_id]['init_pad']
        lstgame[self.room_id]['ball_speed'] = lstgame[self.room_id]['init_ball_speed'] 
        lstgame[self.room_id]['ball_x'] = lstgame[self.room_id]['startXBall']
        lstgame[self.room_id]['ball_y'] = lstgame[self.room_id]['startYBall']
        lstgame[self.room_id]['future_x'] = lstgame[self.room_id]['ball_x']
        lstgame[self.room_id]['future_y'] = lstgame[self.room_id]['ball_y']
        await self.sendBall_remote(lstgame[self.room_id]['ball_x'], lstgame[self.room_id]['ball_y'])
        await self.sendPadInit_remote()
        await asyncio.sleep(1)

    async def  victory_remote(self):
        if (lstgame[self.room_id]['future_x'] < 6.983):
            await self.sendPts_remote("updatePts", "2")
            lstgame[self.room_id]['ball_angle'] = 180
            await self.begin_point_remote()
        else:
            await self.sendPts_remote("updatePts", "1")
            lstgame[self.room_id]['ball_angle'] = 0
            await self.begin_point_remote()

    async def sendwallHitRemote(self):
        await self.channel_layer.group_send(
            self.room_id,
            {
                'type': 'wall_HitRemote',
            }
        )
    
    async def wall_HitRemote(self, event):
        await self.send(text_data=json.dumps({
            'type': 'wallHit',
        }))


    async def wall_collisions_remote(self):
        if (lstgame[self.room_id]['future_x'] < lstgame[self.room_id]['board_min'] + lstgame[self.room_id]['ball_radius'] or lstgame[self.room_id]['future_x'] + lstgame[self.room_id]['ball_radius'] > lstgame[self.room_id]['board_x_max']):
            await self.victory_remote()
            return (1)
        if (lstgame[self.room_id]['future_y'] < lstgame[self.room_id]['board_min'] + lstgame[self.room_id]['ball_radius']):
            lstgame[self.room_id]['future_y'] = lstgame[self.room_id]['board_min'] + lstgame[self.room_id]['ball_radius']
            lstgame[self.room_id]['ball_angle'] *= -1
            await self.sendwallHitRemote()

        if (lstgame[self.room_id]['future_y'] > lstgame[self.room_id]['board_y_max'] - lstgame[self.room_id]['ball_radius']):
            lstgame[self.room_id]['future_y'] = lstgame[self.room_id]['board_y_max'] - lstgame[self.room_id]['ball_radius']
            lstgame[self.room_id]['ball_angle'] *= -1
            await self.sendwallHitRemote()
        lstgame[self.room_id]['ball_x'] = lstgame[self.room_id]['future_x']
        lstgame[self.room_id]['ball_y'] = lstgame[self.room_id]['future_y']
        return (0)

    async def move_ball_remote(self):
        lstgame[self.room_id]['future_x'] = lstgame[self.room_id]['ball_x'] + math.cos(lstgame[self.room_id]['ball_angle'] * math.pi / 180) * lstgame[self.room_id]['ball_speed'] * (lstgame[self.room_id]['boardWidth'] + lstgame[self.room_id]['boardHeight']) / 2000
        lstgame[self.room_id]['future_y'] = lstgame[self.room_id]['ball_y']+ math.sin(lstgame[self.room_id]['ball_angle'] * math.pi / 180) * lstgame[self.room_id]['ball_speed'] * (lstgame[self.room_id]['boardWidth'] + lstgame[self.room_id]['boardHeight']) / 2000
        if await self.wall_collisions_remote() == 0:
            await self.paddle_collisions_remote()

    async def update_baal(self, event):
        x = event['x']
        y = event['y']
        
        await self.send(text_data=json.dumps({
            'type': 'update_baal',
            'x': x,
            'y': y
        }))

    async def sendBall_remote(self, x, y):
        await self.channel_layer.group_send(
                self.room_id,
                {
                    'type': 'update_baal',
                    'x': x ,
                    'y': y ,
                }
            )

    async def loop_game_remote(self):
        print("*-*-*-*-*-*-*thread remote ball*-*-*-*-*-**")
        while lstgame[self.room_id]['Game_on'] != -1:
            while lstgame[self.room_id]['Game_on'] == 1:
                await self.move_ball_remote()
                await self.sendBall_remote(lstgame[self.room_id]['ball_x'], lstgame[self.room_id]['ball_y'])
                await asyncio.sleep(0.005)
            await asyncio.sleep(0.5)


    async def initRemote(self, id):
        # self.redis = await get_redis()
        self.room_id = id
        self.P1Ready = 0
        self.P2Ready = 0
        self.Game_on = 0
        print("l'id est :")
        print(self.room_id)

        if self.room_id not in lstgame:
            lstgame[self.room_id] = {
                'wsj1': None,
                'wsj2': None,
                'boardWidth': 700,
                'boardHeight': 700,
                'AI': 0,
                'init_ball_speed': 4,
                'tick_back': 0.01,
                'Game_on': 0,
                'nb_pts_for_win': 5,
                'P1Ready': 0,
                'P2Ready': 0,
                'PTSp1': 0,
                'PTSp2': 0,
                'xPad1': 10,
                'xPad2': 700 - 30,
                'paddle_width': 20,
                'paddle_height': 140,
                'position_in_paddle': 0,
                'init_pad': 700 / 2 - 140 / 2,
                'posPad1': 700 / 2 - 140 / 2,
                'posPad2': 700 / 2 - 140 / 2,
                'startXBall': 350,
                'startYBall': 350,
                'ball_x': 350,
                'ball_y': 350,
                'future_x': 350,
                'future_y': 350,
                'ball_angle': 180 if random.random() > 0.5 else 0,
                'ball_radius': 7.18,
                'ball_speed': 4,
                'board_y_max': 700,
                'board_x_max': 700,
                'board_min': 0,
                'is_online': 1,
            }

        await self.channel_layer.group_add(
            self.room_id,
            self.channel_name
        )
        self.isRemote = 1        
        await self.sendPts_remote("updatePts", "0")
   


        await self.accept()
        # await self.sendinfo_back("room_id","channel_name", "wsj1")
        # await self.sendinfo_back(self.room_id,self.channel_name, lstgame[self.room_id]['wsj1'])

        if lstgame[self.room_id]['wsj1'] is None:
            print("+++++++++++++++++++j1 join+++++++++++++++")
            lstgame[self.room_id]['wsj1'] = self.channel_name
            print("+++++++++++++++++++j1 join+++++++++++++++")
        if lstgame[self.room_id]['wsj2'] is None:
            print("+++++++++++++++++++j2 join+++++++++++++++")
            lstgame[self.room_id]['wsj2'] = self.channel_name
            print("+++++++++++++++++++j2 join+++++++++++++++")
            asyncio.ensure_future(self.loop_game_remote())

    async def sendStartRemote(self):
        await self.send(text_data=json.dumps({
            'type': "startGame",
        }))
        lstgame[self.room_id]['Game_on'] = 1

# ==========================================================================================================================
# ==========================================================================================================================
#                                                 local play
# ==========================================================================================================================
# ==========================================================================================================================


    async def speed_up_ball(self):
        if (self.AI == 1 and self.ball_speed < 10):
                return (0.2)
        if (self.ball_speed < 12):
            return (0.2)
        return (0)


    async def sendpaddleHit(self):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'paddle_Hit',
            }
        )
    
    async def paddle_Hit(self, event):
        await self.send(text_data=json.dumps({
            'type': 'paddleHit',
        }))



    # async def sendpaddleHit(self):
    #     await self.send(text_data=json.dumps({
    #         'type': "paddleHit",
    #     }))

    async def paddle_collisions(self):
        if (self.future_x <= self.xPad1  + self.paddle_width + self.ball_radius and self.future_x >= self.xPad1  and self.future_y >= self.posPad1 - self.ball_radius and self.future_y <= self.posPad1 + self.paddle_height + self.ball_radius):
            self.position_in_paddle = (2 * (self.ball_y + self.ball_radius - self.posPad1) / (self.paddle_height + self.ball_radius * 2)) - 1
            self.ball_angle = 80 * self.position_in_paddle
            self.ball_x += self.ball_radius / 10
            self.ball_speed += await self.speed_up_ball()
            await self.sendpaddleHit()

        if (self.future_x >= self.xPad2 - self.ball_radius and self.future_x <= self.xPad2 + self.ball_radius / 2 and self.future_y >= self.posPad2 - self.ball_radius and self.future_y <= self.posPad2 + self.paddle_height + self.ball_radius):
            self.position_in_paddle = (2 * (self.ball_y + self.ball_radius - self.posPad2) / (self.paddle_height + self.ball_radius * 2)) - 1
            self.ball_angle = 180 - 80 * self.position_in_paddle
            self.ball_x -= self.ball_radius / 10
            self.ball_speed += await self.speed_up_ball()
            await self.sendpaddleHit()

    async def update_Pts(self, event):
        updatePts = event['updatePts']
        player = event['player']

        await self.send(text_data=json.dumps({
            'type': "updatePts",
            'updatePts': updatePts,
            'player': player,
        }))

    async def sendPts(self, type, player):

        if player == "1":
            self.PTSp1 = self.PTSp1 + 1
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'update_Pts',
                    'updatePts':  self.PTSp1,
                    'player': "1",
                }
            )
            if (self.PTSp1 == self.nb_pts_for_win):
                await self.endGame()
        elif player == "2":
            self.PTSp2 = self.PTSp2 + 1
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'update_Pts',
                    'updatePts':  self.PTSp2,
                    'player': "2",
                }
            )
            if (self.PTSp2 == self.nb_pts_for_win):
                await self.endGame()
    

    async def sendBall(self, x, y):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': "update_Baal",
                'x': x,
                'y': y,
            }
        )

    async def update_Baal(self, event):
        x = event['x']
        y = event['y']

        await self.send(text_data=json.dumps({
            'type': 'updateBaal',
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

        

    async def end_Game(self, event):
        await self.send(text_data=json.dumps({
            'type': 'endGame',
        }))

    async def endGame(self):
        self.Game_on = -1
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'end_Game',
            }
        )
        await self.disconnect(1000)

    async def sendPadInit(self):
        await self.send_mouv_to_group(self.init_pad, "1")
        await self.send_mouv_to_group(self.init_pad, "2")

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
        await asyncio.sleep(1)

    async def  victory(self):
        if (self.future_x < self.boardWidth / 2):
            await self.sendPts("updatePts", "2")
            self.ball_angle = 180
            await self.begin_point()
        else:
            await self.sendPts("updatePts", "1")
            self.ball_angle = 0
            await self.begin_point()

    async def sendwallHit(self):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'wall_Hit',
            }
        )
    
    async def wall_Hit(self, event):
        await self.send(text_data=json.dumps({
            'type': 'wallHit',
        }))


    async def wall_collisions(self):
        if (self.future_x < self.board_min + self.ball_radius or self.future_x + self.ball_radius > self.board_x_max):
            await self.victory()
            return (1)
        if (self.future_y < self.board_min + self.ball_radius):
            self.future_y = self.board_min + self.ball_radius
            self.ball_angle *= -1
            await self.sendwallHit()
        if (self.future_y > self.board_y_max - self.ball_radius):
            self.future_y = self.board_y_max - self.ball_radius
            self.ball_angle *= -1
            await self.sendwallHit()
        self.ball_x = self.future_x
        self.ball_y = self.future_y
        return (0)

    async def move_ball(self):
        self.future_x = self.ball_x + math.cos(self.ball_angle * math.pi / 180) * self.ball_speed * (self.boardWidth + self.boardHeight) / 2000
        self.future_y = self.ball_y + math.sin(self.ball_angle * math.pi / 180) * self.ball_speed * (self.boardWidth + self.boardHeight) / 2000
        if await self.wall_collisions() == 0:
            await self.paddle_collisions()

    async def loop_game(self):
        while self.Game_on != -1:
            while(self.Game_on == 1):
                await self.move_ball()
                await self.sendBall(self.ball_x, self.ball_y)
                await asyncio.sleep(self.tick_back)
            await asyncio.sleep(0.5)

    async def initForLocal(self):
        self.boardWidth = 700
        self.boardHeight = 700
        self.AI = 0
        self.isRemote = 0
        self.init_ball_speed = 6
        self.tick_back = 0.01

        self.Game_on = 0
        self.nb_pts_for_win = 5

        self.P1Ready = 0
        self.P2Ready = 0
        self.PTSp1 = 0
        self.PTSp2 = 0
        self.xPad1 = 10
        self.xPad2 = 700 - 30
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
        self.board_min = 0
        self.is_online = 0
        self.room_id = -1


        # ⊱━━━.⋅εïз⋅.━━━⊰   AI   ⊱━━━.⋅εïз⋅.━━━⊰ #
        self.begin_time = datetime.now().timestamp()
        self.current_time = datetime.now().timestamp()
        self.random_paddle_pos = random.random() * 1000 % self.paddle_height
        self.ball_future_position = self.ball_x
        self.ball_last_direction = -1 if self.ball_angle == 180 else 1
        asyncio.ensure_future(self.loop_game())


    async def sendPadUp(self, player):
        if self.is_online == 0:
            if player == 1:
                self.P1Ready = 1
                self.posPad1 -= 5
                if self.posPad1 < 0:
                    self.posPad1 = 0
                newY = self.posPad1
                await self.send_mouv_to_group(newY, player)
            elif player == 2:
                self.P2Ready = 1
                self.posPad2 -= 5
                if self.posPad2 < 0:
                    self.posPad2 = 0
                newY = self.posPad2
                await self.send_mouv_to_group(newY, player)

        else:
            if player == 1:
                lstgame[self.room_id]['P1Ready'] = 1
                lstgame[self.room_id]['posPad1'] -= 5
                if lstgame[self.room_id]['posPad1'] < 0:
                    lstgame[self.room_id]['posPad1'] = 0
                newY = lstgame[self.room_id]['posPad1']
                await self.send_mouv_to_group(newY, player)
            if player == 2:
                lstgame[self.room_id]['P2Ready'] = 1
                lstgame[self.room_id]['posPad2'] -= 5
                if lstgame[self.room_id]['posPad2'] < 0:
                    lstgame[self.room_id]['posPad2'] = 0
                newY = lstgame[self.room_id]['posPad2']
                await self.send_mouv_to_group(newY, player)



    async def send_mouv_to_group(self, newY, player):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'mouv_down',
                'newY': newY,
                'player': player,
            }
        )

    async def mouv_down(self, event):
        newY = event['newY']
        player = event['player']
        await self.send(text_data=json.dumps({
            'type': 'updatePaddle',
            'newY': newY,
            'player': player,
        }))   

    async def sendPadDown(self, player):
        if self.is_online == 0:
            if player == 1:
                self.P1Ready = 1
                self.posPad1 += 5
                if self.posPad1 > 560:
                    self.posPad1 = 560
                newY = self.posPad1
                await self.send_mouv_to_group(newY, player)
            if player == 2:
                self.P2Ready = 1
                self.posPad2 += 5
                if self.posPad2 > 560:
                    self.posPad2 = 560
                newY = self.posPad2
                await self.send_mouv_to_group(newY, player)
        else:
            if player == 1:
                lstgame[self.room_id]['P1Ready'] = 1
                lstgame[self.room_id]['posPad1'] += 5
                if lstgame[self.room_id]['posPad1'] > 560:
                    lstgame[self.room_id]['posPad1'] = 560
                newY = lstgame[self.room_id]['posPad1']
                await self.send_mouv_to_group(newY, player)
            if player == 2:
                lstgame[self.room_id]['P2Ready'] = 1
                lstgame[self.room_id]['posPad2'] += 5
                if lstgame[self.room_id]['posPad2'] > 560:
                    lstgame[self.room_id]['posPad2'] = 560
                newY = lstgame[self.room_id]['posPad2']
                await self.send_mouv_to_group(newY, player)



    async def sendStart(self):
        await self.send(text_data=json.dumps({
            'type': "startGame",
        }))
        self.Game_on = 1


# ==========================================================================================================================
# ==========================================================================================================================
#                                                 connect
# ==========================================================================================================================
# ==========================================================================================================================


    async def connect(self):
        query_string = self.scope['query_string'].decode('utf-8')
        query_params = urllib.parse.parse_qs(query_string)
        self.room_name = query_params.get('page', [''])[0]
        self.room_group_name = f"game_{self.room_name}"
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        if self.room_name.startswith("game_") or self.room_name.startswith("ia"):
            print("is local")
            await self.initForLocal()
            await self.accept()
            await self.send(text_data=json.dumps({
                'type': 'connection_success',
                'message': 'Connexion réussie!'
            })) 
        elif self.room_name.startswith("remote_"):
            print("is websocket")
            self.is_online = 1
            page_url = self.room_name.replace("remote_", "")
            await self.initRemote(page_url)


    async def receive_test_message(self, event):
        message = event['message']
        # Envoie le message reçu au client WebSocket
        await self.send(text_data=json.dumps(message))

        # await self.send(text_data=json.dumps({
        #     'type': 'connection_success',
        #     'message': 'Connexion réussie!'
        # }))
    

    async def disconnect(self, close_code):
        self.Game_on = 0
        await self.send(text_data=json.dumps({
            'type': 'disconnect',
            'close_code': close_code
        }))

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            type = data.get('type')
            player = int(data.get('player', 0))
            if type and player:
                print("je rentre pas la ? ")
                if type == "mouvUp":
                    await self.sendPadUp(player)
                elif type == "mouvDown":
                    await self.sendPadDown(player)
                elif type == "GameIA":
                    self.AI = 1
                    self.P2Ready = 1
                    self.nb_pts_for_win = 5
                    asyncio.ensure_future(self.ai_loop_game())
                elif type == "pointInit":
                    p1PTS = int(data.get('p1PTS', 0))
                    p2PTS = int(data.get('p2PTS', 0))
                    self.PTSp1 = p1PTS
                    self.PTSp2 = p2PTS
                
            if self.P1Ready == 1 and self.P2Ready == 1 and self.Game_on == 0:
                await self.sendStart()
            if self.is_online == 1:
                if lstgame[self.room_id]['P1Ready'] == 1 and lstgame[self.room_id]['P2Ready'] == 1 and lstgame[self.room_id]['Game_on'] == 0:
                    await self.sendStartRemote()

        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({
                'error': 'Format JSON invalide'
            }))
