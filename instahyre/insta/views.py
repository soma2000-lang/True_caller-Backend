from django.shortcuts import render
# Create your views here.
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework import status
from django.contrib.auth import authenticate
from .models import UserContact, UserContactMapping, UserProfile
from .serializers import ContactSerializer
from rest_framework.views import APIView
from django.db.models import Q
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
class UserContactList(APIView):
    def get(self, request):
        contacts = UserContact.objects.all()
        serializer = ContactSerializer(contacts, many=True)
        return Response(serializer.data)

    def post(self, request):
        # if request.data["name"] is None or request.data["phone_number"] is None:
        #     return Response(
        #         {
        #             "Error": "please provide both name and the phone number"
        #         },
        #         status=status.HTTP_400_BAD_REQUEST
        #     )
        name = request.data.get('name', None)
        phone_number = request.data.get('phone_number', None)
        email = request.data.get('email', None)
        contact = UserContact(
            name=name,
            phone_number=phone_number,
            email=email
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
# @permission_classes((AllowAny,))
# class RegisterList(APIView):
#     def post(self, request):  # Fixed missing request parameter
        
#         username = request.data.get('username', None)
#         password = request.data.get('password', None)
#         email = request.data.get('email', None)
#         phone_number = request.data.get('phone_number', None)
#         user = User(
#             username=username,
#             password=password,
#             email=email
#         )
#         user.set_password(password)
#         user.save()
#         user_profile = UserProfile(
#             user=user,
#             phone_number=phone_number
#         ).save()
#         if (user and user_profile):
#             return Response(
#                 {
#                     "Message": "Registered successfully"
#                 },
#                 status=status.HTTP_200_OK,
#                 content_type="application/json"
#             )
#         else:
#             return Response(
#                 {
#                     "Message": "Error ,Try again"
#                 },
#                 status=status.HTTP_400_BAD_REQUEST,
#                 content_type="application/json"
#             )

# @method_decorator(csrf_exempt, name='dispatch')
# @permission_classes((AllowAny,))
# class RegisterList(APIView):
#     def post(self, request):
#         username = request.data.get('username')
#         password = request.data.get('password')
#         email = request.data.get('email')
#         phone_number = request.data.get('phone_number')

#         # Validate required fields
#         if not all([username, password, email, phone_number]):
#             return Response(
#                 {
#                     "error": "All fields (username, password, email, phone_number) are required"
#                 },
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         # Check if username already exists
#         if User.objects.filter(username=username).exists():
#             return Response(
#                 {
#                     "error": "Username already exists"
#                 },
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         # Check if email already exists
#         if User.objects.filter(email=email).exists():
#             return Response(
#                 {
#                     "error": "Email already exists"
#                 },
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         try:
#             # Create user
#             user = User(
#                 username=username,
#                 email=email
#             )
#             user.set_password(password)
#             user.save()

#             # Create user profile
#             user_profile = UserProfile(
#                 user=user,
#                 phone_number=phone_number
#             )
#             user_profile.save()

#             # Create token for the new user
#             token, _ = Token.objects.get_or_create(user=user)

#             return Response(
#                 {
#                     "message": "Registered successfully",
#                     "token": token.key,
#                     "user": {
#                         "username": user.username,
#                         "email": user.email,
#                         "phone_number": phone_number
#                     }
#                 },
#                 status=status.HTTP_201_CREATED
#             )

#         except Exception as e:
   
#             if 'user' in locals():
#                 user.delete()
            
#             return Response(
#                 {
#                     "error": f"Registration failed: {str(e)}"
#                 },
#                 status=status.HTTP_400_BAD_REQUEST
#             )


class RegisterList(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')
        phone_number = request.data.get('phone_number')

        if not all([username, password, email, phone_number]):
            return Response(
                {"error": "All fields (username, password, email, phone_number) are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({"error": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User(username=username, email=email)
            user.set_password(password)
            user.save()

            user_profile = UserProfile(user=user, phone_number=phone_number)
            user_profile.save()

            token, _ = Token.objects.get_or_create(user=user)

            return Response(
                {"message": "Registered successfully", "token": token.key},
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@permission_classes((AllowAny,))
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
    # permission_classes = [IsAuthenticated]
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
    # permission_classes = [IsAuthenticated]
    
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
                "email": profile.email
            })
            
        except UserProfile.DoesNotExist:
            contacts = UserContact.objects.filter(phone_number=phone_number)
            serializer = ContactSerializer(contacts, many=True)
            return Response(serializer.data)

class SpamSearchList(APIView):
 

    def get(self, request):
        name = request.GET.get('name', None)
        phone_number = request.GET.get('phone_number', None)

        if not any([name, phone_number]):
            return Response(
                {"error": "Please provide either name or phone number"},
                status=status.HTTP_400_BAD_REQUEST
            )

       
        response_data = {
            "name": None,
            "phone_number": None,
            "spam": False,
            "spam_likelihood": "Unknown",
            "is_registered": False,
            "email": None
        }

      
        contact_query = Q()
        if name:
            contact_query |= Q(name=name)
        if phone_number:
            contact_query |= Q(phone_number=phone_number)


        contact = UserContact.objects.filter(contact_query).first()
        if contact:
            response_data.update({
                "name": contact.name,
                "phone_number": contact.phone_number,
                "spam": contact.spam
            })

            spam_reports = UserContact.objects.filter(
                phone_number=contact.phone_number, 
                spam=True
            ).count()

            response_data["spam_likelihood"] = (
                'High' if spam_reports > 2 
                else 'Medium' if spam_reports > 0 
                else 'Low'
            )

            try:
    
                user_profile = UserProfile.objects.get(phone_number=contact.phone_number)
                user = User.objects.get(id=user_profile.user_id)
                response_data["is_registered"] = True


                is_in_contacts = UserContactMapping.objects.filter(
                    user=user,
                    contact__in=UserContact.objects.filter(
                        phone_number=request.user.userprofile.phone_number
                    )
                ).exists()

                
                if is_in_contacts:
                    response_data["email"] = user.email

                if user_profile.spam:
                    response_data["spam_likelihood"] = "High"

            except (UserProfile.DoesNotExist, User.DoesNotExist):
                pass

            return Response(response_data, status=status.HTTP_200_OK)

        return Response(
            {"error": "Contact not found"},
            status=status.HTTP_404_NOT_FOUND
        )
        