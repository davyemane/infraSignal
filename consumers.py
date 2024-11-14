# consumers.py
import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

class NotificationConsumer(WebsocketConsumer):
    def connect(self):
        async_to_sync(self.channel_layer.group_add)(
            "notification_group",
            self.channel_name
        )
        self.accept()
        # Envoyez un message de test à la connexion
        self.send(text_data=json.dumps({
            'type': 'connection_established',
            'message': 'Connecté au serveur WebSocket'
        }))

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            "notification_group",
            self.channel_name
        )

    # Ajoutez cette méthode
    def send_notification(self, event):
        # Envoie le message au client WebSocket
        message = event.get('message', '')
        self.send(text_data=json.dumps({
            'type': 'notification',
            'message': message
        }))
    # Gestionnaire pour les notifications de connexion
    def user_login(self, event):
        self.send(text_data=json.dumps(event))

    # Gestionnaire pour les notifications d'échec de connexion
    def user_login_failed(self, event):
        self.send(text_data=json.dumps(event))

    # Gestionnaire pour les notifications d'inscription
    def user_registered(self, event):
        self.send(text_data=json.dumps(event))

    # Gestionnaire pour les notifications d'échec d'inscription
    def user_register_failed(self, event):
        self.send(text_data=json.dumps(event))