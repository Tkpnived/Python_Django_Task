from django.urls import path
from Taskapp import views


urlpatterns = [
    path('',views.loginpage,name="loginpage"),
    path('Register', views.Register, name="Register"),
    path('user', views.user, name="user"),
    path('userpage', views.userpage, name="userpage"),
    path('logout', views.logout, name="logout"),
    path('edit', views.edit, name="edit"),
    path('updatepassword', views.updatepassword, name="updatepassword"),
]