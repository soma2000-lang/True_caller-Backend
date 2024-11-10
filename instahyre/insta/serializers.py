from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User



class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserContact
        fields = '__all__'