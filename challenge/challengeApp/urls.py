from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name="login"),
    # login it's duplicated because I don't have 
    # a home page.
    path('', views.login, name="login"),
    path('signup/', views.signup, name="signup"),
    path('gadata/', views.gadata,  name='gadata'),
    path('log/', views.log,  name='log'),
    path('home/', views.home, name='home'),
    path('', views.logout, name='logout'),
]
