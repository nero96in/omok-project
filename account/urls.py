from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name="signup"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('ranking/',views.ranking, name="ranking"),
    # path('search/',views.search,name="search"),
    #url(r'^search', SearchFormView.as_view, name='search'),
    
]

