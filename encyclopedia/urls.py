from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("new", views.new, name="new"),
    path("edited", views.change, name="change"),
    path("random", views.random, name="random"),
    path("<str:title>", views.get, name="get"),
    path("<str:ent>/edit", views.edit, name="edit"),
    
]
