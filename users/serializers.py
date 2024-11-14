from .models import *
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

class ProblemTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProblemType
        fields = ['id', 'name', 'description', 'icon']

class PointImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PointImage
        fields = ['id', 'sensitive_point', 'file', 'description', 'uploaded_at']
class SensitivePointSerializer(serializers.ModelSerializer):
    images = PointImageSerializer(many=True, read_only=True)
    created_by = serializers.ReadOnlyField(source='created_by.phone_number')
    latitude = serializers.FloatField(write_only=True)
    longitude = serializers.FloatField(write_only=True)

    class Meta:
        model = SensitivePoint
        fields = ['id', 'created_by', 'problem_type', 'latitude', 'longitude',
                 'sector', 'description', 'status', 'created_at', 
                 'updated_at', 'images']
        read_only_fields = ['created_at', 'updated_at', 'status']

    def create(self, validated_data):
        lat = validated_data.pop('latitude')
        lng = validated_data.pop('longitude')
        location = Point(lng, lat)  # GIS Point expects (longitude, latitude)
        return SensitivePoint.objects.create(
            location=location,
            **validated_data
        )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['latitude'] = instance.location.y
        representation['longitude'] = instance.location.x
        representation['problem_type'] = ProblemTypeSerializer(instance.problem_type).data
        return representation

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
