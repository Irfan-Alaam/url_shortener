from django.urls import path
from .views import create_url_view, list_urls_view, delete_url_view, redirect_short_url,edit_url_view

urlpatterns = [
    path('create/', create_url_view, name='create-url'),
    path('my-urls/', list_urls_view, name='list-urls'),
    path("edit/<int:url_id>/", edit_url_view, name="edit-url"),
    path('delete/<int:url_id>/', delete_url_view, name='delete-url'),
    path('<str:short_key>/', redirect_short_url, name='redirect'),
]
