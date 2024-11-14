from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

class NotificationMixin:
    def send_notification(self, type_message, content):
        try:
            print(f"Tentative d'envoi de notification: {content}")
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "notification_group",
                {
                    "type": "send_notification",  # Assurez-vous que ceci correspond au nom de la méthode dans le consumer
                    "message": content
                }
            )
            print("Notification envoyée avec succès")
        except Exception as e:
            print(f"Erreur WebSocket détaillée: {str(e)}")
            import traceback
            print(traceback.format_exc())