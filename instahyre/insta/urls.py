from django.urls import path
from insta.views import (
    UserContact, Register, Login, Spam,
    SearchName, SearchPhone,SpamSearch)


urlpatterns = [
    path('contacts/', UserContact.as_view(), name='contacts'),
    path('register/', Register.as_view(), name='register'),
    path('login/', Login.as_view(), name='login'),
    path('spam/', Spam.as_view(), name='spam'),
    path('search_name/', SearchName.as_view(), name='search_name'),
    path('search_phone/', SearchPhone.as_view(), name='search_phone'),
    path('search_spam/',  SpamSearch.as_view(), name='search_spam'),

]