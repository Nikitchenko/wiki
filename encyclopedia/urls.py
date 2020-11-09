from django.urls import path

from . import views

#app_name = "wiki"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>", views.article, name="article"),
    path("wiki/newArticle/add", views.add, name="add"),
    path("wiki/<str:entry>/edit", views.edit, name="edit"),
]
