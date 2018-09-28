from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:app_id>/', views.detail, name='detail'),
    path('update/', views.save_app_config, name='save_app_config')
]
