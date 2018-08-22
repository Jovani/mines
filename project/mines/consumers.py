import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from mines.models import MinesweeperGame

class MinesConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = 'mines_{}'.format(self.room_name)

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

    def receive(self, text_data):
        data = json.loads(text_data)
        
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'tile_flip',
                'data': data
            }
        )

    # Receive message from room group
    def tile_flip(self, event):
        data = event['data']

        game = MinesweeperGame.objects.get(id=data['game_id'])
        game.flip_squares_and_save(
            data['x'],
            data['y']
        )
        response = {
            'obscured_game_state': game.obscured_game_state,
            'state': game.state,
        }

        self.send(text_data=json.dumps(response))
