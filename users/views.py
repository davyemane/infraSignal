# views.py
from rest_framework import generics,viewsets, status, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.contrib.auth import authenticate
from .serializers import *
from .models import *
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.decorators import action
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from asgiref.sync import async_to_sync
from rest_framework_simplejwt.views import TokenRefreshView
from .serializers import (
    SensitivePointSerializer,
    ProblemTypeSerializer,
    PointImageSerializer
)
from .mixing import NotificationMixin  # Assurez-vous que le chemin d'importation est correct


class ProblemTypeViewSet(viewsets.ModelViewSet):
    queryset = ProblemType.objects.all()
    serializer_class = ProblemTypeSerializer
    permission_classes = [permissions.IsAuthenticated]

class SensitivePointViewSet(viewsets.ModelViewSet, NotificationMixin):
    serializer_class = SensitivePointSerializer
    # permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser, JSONParser)  # Ajout de JSONParser

    def get_queryset(self):
        queryset = SensitivePoint.objects.all()
        
        # Filtrage par type de problème
        problem_type = self.request.query_params.get('problem_type', None)
        if problem_type:
            queryset = queryset.filter(problem_type=problem_type)
        
        # Filtrage par rayon
        lat = self.request.query_params.get('lat', None)
        lng = self.request.query_params.get('lng', None)
        radius = self.request.query_params.get('radius', None)
        
        if all([lat, lng, radius]):
            point = Point(float(lng), float(lat))
            queryset = queryset.filter(location__distance_lte=(point, D(m=float(radius))))
        
        return queryset

    def perform_create(self, serializer):
        point = serializer.save(created_by=self.request.user)
        
        # Envoi de la notification via WebSocket
        self.send_notification(
            "send_notification",
            f"Nouveau point sensible signalé dans {point.sector}"
        )

    @action(detail=True, methods=['post', 'get'])
    def add_file(self, request, pk=None):
        point = self.get_object()
        serializer = PointImageSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(sensitive_point=point)
            # Notification d'ajout de fichier
            self.send_notification(
                "send_notification",
                f"Un fichier a été ajouté pour le point sensible {point.id}"
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        point = self.get_object()
        new_status = request.data.get('status')
        
        if new_status in dict(SensitivePoint.status.field.choices):
            point.status = new_status
            point.save()
            
            # Notification de changement de statut
            self.send_notification(
                "send_notification",
                f"Le statut du point sensible {point.id} a été mis à jour à {new_status}"
            )
            
            return Response({'status': new_status})
        return Response(
            {'error': 'Invalid status'},
            status=status.HTTP_400_BAD_REQUEST
        )
# class NotificationMixin:
#     def send_notification(self, type_message, content):
#         try:
#             channel_layer = get_channel_layer()
#             async_to_sync(channel_layer.group_send)(
#                 "notification_group",
#                 {
#                     "type": type_message,
#                     "message": content
#                 }
#             )
#         except Exception as e:
#             print(f"Erreur WebSocket: {str(e)}")

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
            
class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        try:
            serializer.is_valid(raise_exception=True)
            
            return Response({
                'access': serializer.validated_data['access'],
                'refresh': request.data['refresh']  # Renvoie aussi le refresh token
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_401_UNAUTHORIZED)