from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    # By ahmederrami@gmail.com
    path("wiki/<str:title>", views.entry, name="entry"),
    path("search", views.search, name="search"),
    path("add", views.add, name="add"),
    path("edit/<str:title>", views.edit, name='edit'),
    path("save", views.save, name="save"),
    path("random", views.randomEntry, name="randomEntry")
]
