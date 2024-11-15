import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import logging

logger = logging.getLogger(__name__)

class NotificationConsumer(WebsocketConsumer):
    def connect(self):
        logger.info("Tentative de connexion WebSocket")
        self.group_name = "notification_group"
        
        # Rejoindre le groupe
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )
        
        self.accept()
        logger.info("Connexion WebSocket acceptée")
        
        # Message de test
        self.send(text_data=json.dumps({
            'type': 'connection_established',
            'message': 'Connecté au serveur WebSocket'
        }))

    def disconnect(self, close_code):
        logger.info(f"Déconnexion WebSocket avec code: {close_code}")
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )

    def receive(self, text_data):
        logger.info(f"Message reçu: {text_data}")
        try:
            text_data_json = json.loads(text_data)
            message = text_data_json['message']
            
            # Diffuser au groupe
            async_to_sync(self.channel_layer.group_send)(
                self.group_name,
                {
                    'type': 'send_notification',
                    'message': message
                }
            )
        except json.JSONDecodeError:
            logger.error("Message reçu n'est pas un JSON valide")
        except KeyError:
            logger.error("Message reçu ne contient pas la clé 'message'")

    def send_notification(self, event):
        logger.info(f"Envoi de notification: {event}")
        message = event.get('message', '')
        self.send(text_data=json.dumps({
            'type': 'notification',
            'message': message
        }))

    def user_login(self, event):
        logger.info(f"Login notification: {event}")
        self.send(text_data=json.dumps(event))

    def user_login_failed(self, event):
        logger.info(f"Login failed notification: {event}")
        self.send(text_data=json.dumps(event))

    def user_registered(self, event):
        logger.info(f"Registration notification: {event}")
        self.send(text_data=json.dumps(event))

    def user_register_failed(self, event):
        logger.info(f"Registration failed notification: {event}")
        self.send(text_data=json.dumps(event))