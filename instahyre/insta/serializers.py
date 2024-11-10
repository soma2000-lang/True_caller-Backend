from rest_framework import serializers
from .models import UserProfile,UserContact,UserContactMapping
from django.contrib.auth.models import User



class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserContact
        fields = '__all__'