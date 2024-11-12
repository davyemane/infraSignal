from .models import CustomUser
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('phone_number', 'password')

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            phone_number=validated_data['phone_number'],
            password=validated_data['password']
        )
        return user
