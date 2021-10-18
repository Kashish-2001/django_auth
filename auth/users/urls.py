from django.urls import path
from .views import RegisterView, LoginView, GetUser

urlpatterns = [
    path('register', RegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('get-user', GetUser.as_view())
]
