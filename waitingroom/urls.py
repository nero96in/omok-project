from django.urls import path
# from .views import SearchFormView
from . import views 

urlpatterns = [
    path('', views.waitingroom, name="waitingroom"),
    path('<room_name>/', views.addroom, name='room'),
]