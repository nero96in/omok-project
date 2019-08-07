from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
from omok_main.SongOmok import Omok
from omok_main.models import Room
import numpy as np
import json
import random


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.omok = Omok()
        
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        self.user = self.scope["user"]
        print(self.user)

        # 룸이 이미 존재하는지 확인.
        if Room.objects.filter(room_name=self.room_name):
            self.room = Room.objects.get(room_name=self.room_name)
            if self.room.player1:
                self.room.player2 = str(self.user)
                self.room.save()
                
                play_order = random.sample([self.room.player1, self.room.player2], 2)
                start_settings = {
                    'black': play_order[0],
                    'white': play_order[1],
                }
                await self.accept()
                await self.send(text_data=json.dumps({
                    'start_settings': start_settings
                }))
            # else:
            #     self.room.player1 = str(self.user)
            #     self.room.save()
            #     await self.accept()
        else:
            new_room = Room(room_name=self.room_name)
            new_room.save()
            self.room = Room.objects.get(room_name=self.room_name)
            self.room.player1 = str(self.user)
            self.room.save()
            await self.accept()

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )
        
        # await self.channel_layer.group_send(
        #         self.room_group_name,
        #         {
        #             'type': 'start_settings',
        #             'start_settings': start_settings
        #         }
        #     )
        # if self.room.player1:
        #     self.send(text_data=json.dumps({
        #                 'start_settings': start_settings
        #             }))
        # if Black == None: Black = 1
        # else: White = 2
        
        # print(Black, White)

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        # self.user_num -= 1
        # print(self.user_num)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        if 'message' in text_data_json.keys():
            message = text_data_json['message']
            print(message)
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
            
            self.omok.Draw()
            print(col,row,digonal_1,digonal_2)

            if self.omok.Rule_Omok(col,row,digonal_1,digonal_2) == 'exit':
                print(self.omok.Color , " Win!")
                message['alert'] = self.omok.Color , " Win!"
                # break
            elif sum_of_sam > 1:
                print("SamSam !! Try Again ! ")
                self.omok.board[self.omok.y][self.omok.x] = 0
                message['alert'] = "SamSam !! Try Again ! "
                # continue
            # self.omok.Playerchange()

        elif 'username' in text_data_json.keys():
            username = text_data_json['username']
            # await self.channel_layer.group_send(
            #     self.room_group_name,
            #     {
            #         'type': 'chat_message',
            #         'username': username,
            #     }
            # )
        # Send message to room group
    

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))

    async def start_settings(self, event):
        start_settings = event['start_settings']
        await self.send(text_data=json.dumps({
            'start_settings': start_settings
        }))