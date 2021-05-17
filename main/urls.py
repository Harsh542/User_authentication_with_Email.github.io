from django.urls import path
from . import views

urlpatterns = [
    path('', views.login , name="login"),
    path('signUp/', views.signUp , name="signUp"),
    path('verify/<token>', views.verify , name="verify"),
    path('home/', views.home, name="home"),
    path('error/', views.error, name="error"),
    path('logout/', views.logout, name="logout"),
]