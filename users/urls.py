from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.RegUser.as_view(), name='reg'),
    path('login/', views.Login.as_view(), name='log'),
    path('logout/', LogoutView.as_view(next_page='users:log'), name='logout'),
]
