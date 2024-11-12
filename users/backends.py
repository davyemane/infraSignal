from django.contrib.auth.backends import ModelBackend
from .models import CustomUser
import os
import django

# Spécifie le chemin de ton fichier settings.py
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'infraSignal.settings')

# Initialise Django
django.setup()


class PhoneNumberAuthBackend(ModelBackend):
    def authenticate(self, request, phone_number=None, password=None, **kwargs):
        try:
            user = CustomUser.objects.get(phone_number=phone_number)
            if user.check_password(password):
                return user
        except CustomUser.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None
