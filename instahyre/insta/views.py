from django.shortcuts import render
# Create your views here.
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework import status
from django.contrib.auth import authenticate
from .models import UserContact, UserContactMapping, UserProfile
from .serializers import ContactSerializer
from rest_framework.views import APIView
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
class UserContactList(APIView):
    def get(self, request):
        contacts = UserContact.objects.all()
        serializer = ContactSerializer(contacts, many=True)
        return Response(serializer.data)

    def post(self, request):
        if request.data["name"] is None or request.data["phone_number"] is None:
            return Response(
                {
                    "Error": "please provide both name and the phone number"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        name = request.data.get('name', None)
        phone_number = request.data.get('phone_number', None)
        email_address = request.data.get('email_address', None)
        contact = UserContact(
            name=name,
            phone_number=phone_number,
            email_address=email_address
        )
        contact.save()
        # creating the mapping
        mapping = UserContactMapping(
            user=request.user,
            contact=contact
        ).save()
        response = {
            'data': request.data
        }
        return Response(
            response,
            status=status.HTTP_201_CREATED,
            content_type="application/json"
        )

class RegisterList(APIView):
    def post(self, request):  # Fixed missing request parameter
        if request.data["name"] is None or request.data["phone_number"] is None:
            return Response(
                {
                    "Error": "please provide both name and the phone number, either of the 2 are missing"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        username = request.data.get('username', None)
        password = request.data.get('password', None)
        email_address = request.data.get('email_address', None)
        phone_number = request.data.get('phone_number', None)
        user = User(
            username=username,
            password=password,
            email_address=email_address
        )
        user.set_password(password)
        user.save()
        user_profile = UserProfile(
            user=user,
            phone_number=phone_number
        ).save()
        if (user and user_profile):
            return Response(
                {
                    "Message": "Registered successfully"
                },
                status=status.HTTP_200_OK,
                content_type="application/json"
            )
        else:
            return Response(
                {
                    "Message": "Error ,Try again"
                },
                status=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )

class LoginList(APIView):
    def post(self, request):
        if not request.data:
            return Response(
                {'Error': "Please provide username/password"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        username = request.data.get('username', None)
        password = request.data.get('password', None)
        
        if authenticate(username=username, password=password):
            user = User.objects.get(username=username)
            token, _ = Token.objects.get_or_create(user=user)
            return Response(
                {
                    "Token": token.key
                },
                status=status.HTTP_200_OK
            )
        
        return Response(
            {
                "Error": "Invalid credentials"
            },
            status=status.HTTP_401_UNAUTHORIZED
        )

class SpamList(APIView):
    def post(self, request):
   
            phone_number = request.data.get('phone_number', None)
            if (UserContact.objects.filter(phone_number=phone_number).update(spam=True) and UserProfile.objects.filter(phone_number=phone_number).update(spam=True)):
                return Response(
				{
					"Message":"Contact marked as spam successfully!!"
				},
				status = status.HTTP_200_OK
			)
            else:
                return Response(
                    {
                        "Error":"Phone number not found!!"
                    },
                    status = status.HTTP_404_NOT_FOUND)



class SearchNameList(APIView):
    def get(self, request):
        name = request.GET.get('name', None)
        
        if not name:
            return Response(
                {"Error": "Please provide a name to search"},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        contacts = UserContact.objects.filter(
            Q(name=name) | Q(name__contains=name)
        ).values('name', 'phone_number', 'spam')
        
        return Response(
            list(contacts),
            status=status.HTTP_200_OK
        )

class SearchPhoneList(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        phone_number = request.GET.get('phone_number', None)
        
        if not phone_number:
            return Response(
                {"error": "Phone number is required"}, 
                status=400
            )
            
        try:
            profile = UserProfile.objects.get(phone_number=phone_number)
            user = get_object_or_404(User, id=profile.user_id, is_active=True)
            
            return Response({
             
                "phone_number": profile.phone_number,
                "spam": profile.spam,
                "email_address": profile.email_address
            })
            
        except UserProfile.DoesNotExist:
            contacts = UserContact.objects.filter(phone_number=phone_number)
            serializer = ContactSerializer(contacts, many=True)
            return Response(serializer.data)