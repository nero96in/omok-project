from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name="signup"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('ranking/',views.ranking, name="ranking"),
    path('rank_list_ajax', views.rank_list_ajax, name="rank_list_ajax"),
    
]

