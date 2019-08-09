from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
from omok_main.SongOmok import Omok
from omok_main.models import Room
from account.models import User
import numpy as np
import json
import random


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.omok = Omok()
        self.current_player = 1
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        self.user = self.scope["user"]
        print(self.user)
        # a = User(username=str(self.user))
        # print("win: ", a.win)
        # Join room group

        # 룸이 이미 존재하는지 확인.
        if Room.objects.filter(room_name=self.room_name):
            self.room = Room.objects.get(room_name=self.room_name)
            
            if (self.room.player1 or self.room.player2) and self.room.player1 != str(self.user) and self.room.player2 != str(self.user):
                # 두 플레이어 모두 존재하면 관전자로 입장
                if self.room.player1 and self.room.player2:
                    await self.channel_layer.group_add(
                        self.room_group_name,
                        self.channel_name,
                    )
                    await self.accept()
                    await self.channel_layer.group_send(
                        self.room_group_name,
                        {
                            "type": "spectator_message",
                            "message": str(self.user),
                        }
                    )
                    await self.send(text_data=json.dumps({
                        'type': 'load_board',
                        'load_board': self.room.omok_board
                    }))
                    
                else:
                    if not self.room.player2: self.room.player2 = str(self.user)
                    elif not self.room.player1: self.room.player1 = str(self.user)
                    self.room.is_playing = True
                    self.room.save()
                    
                    self.play_order = random.sample([self.room.player1, self.room.player2], 2)
                    start_settings = {
                        'black': self.play_order[0],
                        'white': self.play_order[1],
                        'current_player': self.current_player,
                        'alert': "match success",
                    }
                    await self.channel_layer.group_add(
                        self.room_group_name,
                        self.channel_name,
                    )
                    await self.accept()
                    await self.channel_layer.group_send(
                        self.room_group_name,
                        {
                            'type': 'update_profile',
                            # 'player1': self.room.player1,
                            # 'player2': self.room.player2,
                        }
                    )
                    await self.channel_layer.group_send(
                        self.room_group_name,
                        {
                            'type': 'start_settings',
                            'start_settings': start_settings,
                        }
                    )
            elif self.room.player1 == str(self.user) or self.room.player2 == str(self.user):
                print("10:", self.room.player1, self.room.player2)
                pass

        else:
            new_room = Room(room_name=self.room_name)
            new_room.save()
            self.room = Room.objects.get(room_name=self.room_name)
            self.room.player1 = str(self.user)
            self.room.save()
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name,
            )
            await self.accept()
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'update_profile',
                    # 'player1': self.room.player1,
                    # 'player2': self.room.player2,
                }
            )
            

    async def disconnect(self, close_code):
        # Leave room group
        self.room = Room.objects.get(room_name=self.room_name)
        if self.room.is_playing:
            self.room.is_playing = False
            lose_user = self.scope["user"].username
            if self.scope["user"].username == self.room.player1:
                self.room.player1 = None
                self.room.save()
                win_user = self.room.player2
            elif self.scope["user"].username == self.room.player2:
                self.room.player2 = None
                self.room.save()
                win_user = self.room.player1

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'end_game',
                    'win_user': win_user,
                    'lose_user': lose_user,
                }
            )
        else:
            if self.scope["user"].username == self.room.player1:
                print(self.scope["user"].username, self.room.player1)
                self.room.player1 = None
                self.room.save()
            if self.scope["user"].username == self.room.player2:
                print(self.scope["user"].username, self.room.player2)
                self.room.player2 = None
                self.room.save()
            if not self.room.player1 and not self.room.player2:
                self.room.delete()
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'update_profile',
                    # 'player1': self.room.player1,
                    # 'player2': self.room.player2,
                }
            )
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        if 'message' in text_data_json.keys():
            self.room = Room.objects.get(room_name=self.room_name)
            message = text_data_json['message']
            # print(message)
            player = message['player']
            x = message['x']
            y = message['y']

            self.omok.Put_omok(player, x, y)
            # print(self.omok.x, self.omok.y)
            col,row,digonal_1,digonal_2 = self.omok.Trace()
            sam_col = self.omok.samsam(col)
            sam_row = self.omok.samsam(row)
            sam_digonal_1 = self.omok.samsam(digonal_1)
            sam_digonal_2 = self.omok.samsam(digonal_2)
            sum_of_sam = sam_col + sam_row + sam_digonal_1 + sam_digonal_2 

            
            self.room.omok_board = self.room.omok_board + str(player) + "," +  str(x) + "," + str(y) + ";"
            self.room.save()
            # print(col,row,digonal_1,digonal_2)

            if self.omok.Rule_Omok(col,row,digonal_1,digonal_2) == 'exit':
                print(self.omok.Color , " Win!")
                message['alert'] = self.omok.Color , " Win!"
                if self.omok.Color == "black":
                    # self.room = Room.objects.get(room_name=self.room_name)
                    win_user = self.play_order[0]
                    lose_user = self.play_order[1]
                elif self.omok.Color == "white":
                    # self.room = Room.objects.get(room_name=self.room_name)
                    win_user = self.play_order[1]
                    lose_user = self.play_order[0]

                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'end_game',
                        'win_user': win_user,
                        'lose_user': lose_user,
                    }
                )
                    
                # break
            elif sum_of_sam > 1:
                print("SamSam !! Try Again ! ")
                self.omok.board[self.omok.y][self.omok.x] = 0
                message['alert'] = "SamSam !! Try Again ! "
                # continue
            print("message:", message)


            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                }
            )

            self.omok.Playerchange()

    async def start_settings(self, event):
        start_settings = event['start_settings']
        await self.send(text_data=json.dumps({
            'type': 'start_settings',
            'start_settings': start_settings
        }))
        
    # Receive message from room group
    async def chat_message(self, event):
        if self.current_player == 1: self.current_player = 2
        elif self.current_player == 2: self.current_player = 1
        message = event['message']
        message['current_player'] = self.current_player
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': message
        }))

    async def spectator_message(self, event):
        spectator = event['message']
        await self.send(text_data=json.dumps({
            'type': 'spectator_message',
            'spectator': spectator
        }))

    async def update_profile(self, event):
        print("3:", self.room.player1, self.room.player2)
        self.room = Room.objects.get(room_name=self.room_name)
        player1 = User(username=self.room.player1)
        player1_info = {
            'username': self.room.player1,
            'win': player1.win,
            'draw': player1.draw, 
            'lose': player1.lose, 
        }
        player2 = User(username=self.room.player2)
        player2_info = {
            'username': self.room.player2,
            'win': player2.win,
            'draw': player2.draw, 
            'lose': player2.lose, 
        }
        print("4:", self.room.player1, self.room.player2)
        await self.send(text_data=json.dumps({
            'type': 'update_profile',
            'player1_info': player1_info,
            'player2_info': player2_info
        }))

    async def end_game(self, evnet):
        win_user = User.objects.get(username=evnet["win_user"])
        lose_user = User.objects.get(username=evnet["lose_user"])
        win_user.win += 1
        lose_user.lose += 1
        win_user.save()
        lose_user.save()
        await self.send(text_data=json.dumps({
            'type': 'end_game',
            'win_user': win_user.username,
            'lose_user': lose_user.username
        }))

    async def load_board(self, evnet):
        pass