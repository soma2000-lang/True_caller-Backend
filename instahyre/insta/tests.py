from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from .models import UserContact, UserProfile, UserContactMapping
from rest_framework.authtoken.models import Token

class ContactAPITests(APITestCase):
    def setUp(self):
        """Initialize test data"""

        self.test_user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@test.com'
        )
        self.test_user_profile = UserProfile.objects.create(
            user=self.test_user,
            phone_number='1234567890'
        )

        self.another_user = User.objects.create_user(
            username='anotheruser',
            password='testpass123',
            email='another@test.com'
        )
        self.another_user_profile = UserProfile.objects.create(
            user=self.another_user,
            phone_number='9876543210'
        )

        self.token = Token.objects.create(user=self.test_user)
        self.another_token = Token.objects.create(user=self.another_user)

   
        self.client = APIClient()
        

        self.test_contact = UserContact.objects.create(
            name='John Doe',
            phone_number='5555555555',
            email='john@test.com'
        )

    def test_register_user(self):
        """Test user registration"""
        url = reverse('register-list')
        data = {
            'username': 'newuser',
            'password': 'newpass123',
            'email': 'new@test.com',
            'phone_number': '1111111111'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue('token' in response.data)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_login_user(self):
        """Test user login"""
        url = reverse('login-list')
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('Token' in response.data)

    def test_add_contact(self):
        """Test adding a new contact"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        url = reverse('user-contact-list')
        data = {
            'name': 'Jane Doe',
            'phone_number': '4444444444',
            'email': 'jane@test.com'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_search_by_name(self):
        """Test searching contacts by name"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        url = reverse('search-name-list')
        response = self.client.get(f"{url}?name=John")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)

    def test_search_by_phone(self):
        """Test searching contacts by phone number"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        url = reverse('search-phone-list')
        response = self.client.get(f"{url}?phone_number=5555555555")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_mark_spam(self):
        """Test marking a contact as spam"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        url = reverse('spam-list')
        data = {
            'phone_number': '5555555555'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_spam_search(self):
        """Test detailed spam search functionality"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        url = reverse('spam-search-list')
        

        response = self.client.get(f"{url}?name=John")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        

        response = self.client.get(f"{url}?phone_number=5555555555")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthorized_access(self):
        """Test endpoints without authentication"""
        urls = [
            reverse('user-contact-list'),
            reverse('search-name-list'),
            reverse('search-phone-list'),
            reverse('spam-list'),
            reverse('spam-search-list')
        ]
        
        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_invalid_registration(self):
        """Test registration with invalid data"""
        url = reverse('register-list')
        

        data = {'username': 'newuser'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        data = {
            'username': 'testuser',  
            'password': 'newpass123',
            'email': 'new@test.com',
            'phone_number': '1111111111'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_email_privacy(self):
        """Test email privacy rules"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        url = reverse('spam-search-list')
        

        UserContactMapping.objects.create(
            user=self.another_user,
            contact=self.test_contact
        )
        
 
        response = self.client.get(f"{url}?phone_number={self.another_user_profile.phone_number}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNone(response.data.get('email'))

        UserContactMapping.objects.create(
            user=self.test_user,
            contact=self.test_contact
        )
        

        response = self.client.get(f"{url}?phone_number={self.test_contact.phone_number}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data.get('email'))

    def test_spam_likelihood(self):
        """Test spam likelihood calculation"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        

        contact = UserContact.objects.create(
            name='Spam User',
            phone_number='7777777777',
            email='spam@test.com'
        )
        
    
        for _ in range(3):a
            UserContact.objects.create(
                name='Spam User',
                phone_number='7777777777',
                spam=True
            )
        
        url = reverse('spam-search-list')
        response = self.client.get(f"{url}?phone_number=7777777777")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['spam_likelihood'], 'High')
