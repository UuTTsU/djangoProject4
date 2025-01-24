from django.urls import path
from .views import Home, RegisterUserView, LoginUser, LogoutUser


urlpatterns = [
    path('', Home.as_view()),
    path('register/', RegisterUserView.as_view()),
    path('login/', LoginUser.as_view()),
    path('logout/', LogoutUser.as_view()),
]