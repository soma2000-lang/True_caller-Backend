from django.db import models

# Create your models here.

from django.contrib.auth.models import User
 


class UserContact(models.Model):
    name=models.CharField(max_length=100, null=False )
    phone_number=models.CharField(max_length=10, null =False)
    email_address=models.EmailField(max_length=100, null=True)
    spam=models.BooleanField(default=False)
    status= models.BooleanField(default=True)

    def __str__(self):
        return self.name



class UserContactMapping(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    contact=models.ForeignKey(UserContact, on_delete=models.CASCADE, null=False)
    status=models.BooleanField(default=True)



    def __str__(self):
        return str(self.user) + ',' + str(self.contact)



class  UserProfile(models.Model):

    user= models.OneToOneField(User, on_delete=models.CASCADE, null=False)
    phone_number= models.CharField(max_length=10, null=False, unique=True)
    email_address=models.EmailField(max_length=100, null=True)
    spam=models.BooleanField(default=False)
    status= models.BooleanField(default=True)

    def __str__(self):
        return str(self.user)