from django.urls import path
from . import views

urlpatterns = [
    path('', views.books_upload, name='books-upload'),
    path('index/', views.index, name='index'),
]