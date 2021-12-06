from django.urls import path

from . import views

urlpatterns = [
    path("search", views.search, name="search"),
    path("new", views.new_entry, name="new"),
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("random", views.random_page, name="random")
]
