# consumers.py
import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

class NotificationConsumer(WebsocketConsumer):
    def connect(self):
        # Ajouter le client au groupe de notification
        async_to_sync(self.channel_layer.group_add)(
            "notification_group",
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        # Retirer le client du groupe de notification
        async_to_sync(self.channel_layer.group_discard)(
            "notification_group",
            self.channel_name
        )

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