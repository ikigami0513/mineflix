from django.urls import path
from . import views


urlpatterns = [
    path('favorites/', views.FavoritesUserList.as_view(), name='favorites_user_view')
]
