from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
from omok_main.SongOmok import Omok
from omok_main.models import Room
from account.models import User
import numpy as np
import json, sys
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
            if self.room.player1: player1_name = self.room.player1.username
            else: player1_name = None
            if self.room.player2: player2_name = self.room.player2.username
            else: player2_name = None
            print("1", self.user)
            print("player1_name:", player1_name)
            print("player2_name:", player2_name)
            print("99", not self.room.player1)
            print("100", not self.room.player2)

            if (self.room.player1 or self.room.player2) and player1_name != str(self.user) and player2_name != str(self.user):
                # 두 플레이어 모두 존재하면 관전자로 입장
                if self.room.player1 and self.room.player2:
                    print("2", self.user)
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
                  
                
                # 둘 중 하나만 존재하지 않을 때.
                else:
                    print("4", self.user)
                    if not self.room.player2: self.room.player2 = User.objects.get(username=str(self.user))
                    elif not self.room.player1: self.room.player1 = User.objects.get(username=str(self.user))
                    self.room.is_playing = True
                    self.room.save()
                    
                    self.play_order = random.sample([self.room.player1, self.room.player2], 2)
                    start_settings = {
                        'black': self.play_order[0].username,
                        'white': self.play_order[1].username,
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
            elif player1_name == str(self.user) or player2_name == str(self.user):
                print("5", self.user)
                await self.accept()
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'update_profile',
                        # 'player1': self.room.player1,
                        # 'player2': self.room.player2,
                    }
                )
                await self.send(text_data=json.dumps({
                        'type': 'load_board',
                        'load_board': self.room.omok_board
                    }))

            # 두 유저 모두 존재하지 않을 때.
            elif (not self.room.player1) and (not self.room.player2):
                print("3", self.user)
                self.room.player1 = User.objects.get(username=str(self.user))
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
        else:
            # new_room = Room(room_name=self.room_name)
            # new_room.save()
            print("9", self.user)
            try: 
                self.room = Room.objects.get(room_name=self.room_name)
                self.room.player1 = User.objects.get(username=str(self.user))
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
            except:
                await self.close()

    async def disconnect(self, close_code):
        # Leave room group
        try: self.room = Room.objects.get(room_name=self.room_name)
        except: self.room = None
    
        if not self.room:
            await self.close()
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )
            
        else:
            if self.room.player1: player1_name = self.room.player1.username
            else: player1_name = None
            if self.room.player2: player2_name = self.room.player2.username
            else: player2_name = None

            # 플레이 도중 연결 끊김.
            if self.room.is_playing:
                # 나간 사람이 이름이 같다면
                if player1_name == self.scope["user"].username or player2_name == self.scope["user"].username:
                    self.room.is_playing = False
                    lose_user = self.scope["user"].username
                    if self.scope["user"].username == player1_name:
                        self.room.player1 = None
                        self.room.save()
                        win_user = player2_name
                    elif self.scope["user"].username == player2_name:
                        self.room.player2 = None
                        self.room.save()
                        win_user = player1_name

                    await self.channel_layer.group_send(
                        self.room_group_name,
                        {
                            'type': 'end_game',
                            'win_user': win_user,
                            'lose_user': lose_user,
                        }
                    )
                # 아니면 관전자일테니 그냥 내보내기
                else:
                    await self.channel_layer.group_send(
                        self.room_group_name,
                        {
                            'type': 'update_profile',
                            # 'player1': self.room.player1,
                            # 'player2': self.room.player2,
                        }
                    )
            
            # 플레이 중이 아님.
            else:
                if self.scope["user"].username == player1_name:
                    print(self.scope["user"].username, player1_name)
                    self.room.player1 = None
                    self.room.save()
                if self.scope["user"].username == player2_name:
                    print(self.scope["user"].username, player2_name)
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
                    win_user = self.play_order[0].username
                    lose_user = self.play_order[1].username
                elif self.omok.Color == "white":
                    # self.room = Room.objects.get(room_name=self.room_name)
                    win_user = self.play_order[1].username
                    lose_user = self.play_order[0].username

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
        # player1 = User(username=self.room.player1)
        player1_info = None
        player2_info = None
        if self.room.player1:
            player1_info = {
                'username': self.room.player1.username,
                'win': self.room.player1.win,
                'draw': self.room.player1.draw, 
                'lose': self.room.player1.lose, 
            }
        # player2 = User(username=self.room.player2)
        if self.room.player2:
            player2_info = {
                'username': self.room.player2.username,
                'win': self.room.player1.win,
                'draw': self.room.player1.draw, 
                'lose': self.room.player1.lose, 
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

