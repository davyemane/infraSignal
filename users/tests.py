from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import CustomUser

class UserTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_register_user(self):
        response = self.client.post(reverse('register'), {
            'phone_number': '1234567890',
            'password': 'motdepassefort'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login_user(self):
        # Enregistre d'abord un utilisateur
        CustomUser.objects.create_user(phone_number='1234567890', password='motdepassefort')
        
        # Test de connexion
        response = self.client.post('/api/token/', {
            'phone_number': '1234567890',
            'password': 'motdepassefort'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
