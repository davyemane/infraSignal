# views.py
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.contrib.auth import authenticate
from .serializers import UserSerializer
from .models import CustomUser

class NotificationMixin:
    def send_notification(self, type_message, content):
        try:
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "notification_group",
                {
                    "type": type_message,
                    "message": content
                }
            )
        except Exception as e:
            print(f"Erreur WebSocket: {str(e)}")

class LoginUserView(NotificationMixin, APIView):
    def post(self, request, *args, **kwargs):
        phone_number = request.data.get("phone_number")
        password = request.data.get("password")

        user = authenticate(request, phone_number=phone_number, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            
            # Envoyer une notification de connexion
            self.send_notification(
                "user.login",
                {
                    "status": "success",
                    "user_id": user.id,
                    "phone_number": user.phone_number,
                    "message": f"Utilisateur {phone_number} connecté"
                }
            )
            
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user_id': user.id,
                'phone_number': user.phone_number
            }, status=status.HTTP_200_OK)
        else:
            # Envoyer une notification d'échec de connexion
            self.send_notification(
                "user.login_failed",
                {
                    "status": "error",
                    "message": f"Tentative de connexion échouée pour {phone_number}"
                }
            )
            
            return Response(
                {"error": "Numéro de téléphone ou mot de passe incorrect"},
                status=status.HTTP_401_UNAUTHORIZED
            )

class RegisterUserView(NotificationMixin, generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            
            # Envoyer une notification d'inscription
            self.send_notification(
                "user.registered",
                {
                    "status": "success",
                    "user_id": user.id,
                    "phone_number": user.phone_number,
                    "message": f"Nouvel utilisateur inscrit: {user.phone_number}"
                }
            )
            
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user_id': user.id,
                'phone_number': user.phone_number
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            # Envoyer une notification d'échec d'inscription
            self.send_notification(
                "user.register_failed",
                {
                    "status": "error",
                    "message": f"Échec d'inscription: {str(e)}"
                }
            )
            
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )