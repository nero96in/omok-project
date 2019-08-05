from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from omok_main.SongOmok import Omok
import numpy as np
import json

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.omok = Omok()
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
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

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
            }
        )

        self.omok.Playerchange()

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))