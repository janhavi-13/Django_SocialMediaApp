from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'profiles'

urlpatterns = [
    path('<str:username>/', views.ProfileDetailView.as_view(), name='detail'),
    path('<str:username>/follow/', views.FollowView.as_view(), name='follow'),
    path('account/change_password', views.change_password, name='change_password'),
]
