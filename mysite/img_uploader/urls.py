from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("new", views.new_image_view, name="new"),
    path("images/<int:img_id>/", views.resize_image_view,
         name="resize"),
]
