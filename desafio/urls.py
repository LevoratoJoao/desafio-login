from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("desafio/login", views.loginView, name="login"),
    path("desafio/register", views.register, name="register"),
    path("desafio/logout", views.logoutView, name="logout"),
]