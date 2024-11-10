from django.urls import path
from insta.views import (
    UserContactList, RegisterList, LoginList, SpamList,
    SearchNameList, SearchPhoneList,SpamSearchList)


urlpatterns = [
    path('contacts/', UserContactList.as_view(), name='contacts'),
    path('register/', RegisterList.as_view(), name='register'),
    path('login/', LoginList.as_view(), name='login'),
    path('spam/', SpamList.as_view(), name='spam'),
    path('search_name/', SearchNameList.as_view(), name='search_name'),
    path('search_phone/', SearchPhoneList.as_view(), name='search_phone'),
    path('search_spam/',  SpamSearchList.as_view(), name='search_spam'),

]