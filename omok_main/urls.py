from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<room_name>/', views.room, name='room')
    # url(r'^$', views.index, name='index'),
]