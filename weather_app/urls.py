from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path("delete/<int:id>/", views.delete) # строка для работы функции удаления через кнопку
]
