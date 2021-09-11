from django.urls import path

from Loginandlogout import views

urlpatterns = [
    path('login/', views.LoginAPI.as_view()),
    path('logout/', views.Logout.as_view()),
    path('register/', views.RegisterAPI.as_view()),
    path('data/', views.StudentDataAPI.as_view()),
]
