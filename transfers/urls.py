from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('ui/upload/', views.upload_page, name='upload_page'),
    path('ui/download/', views.download_page, name='download_page'),
    path('upload/', views.upload_file, name='api_upload'),
    path('download/<str:code>/', views.download_file, name='download_file'),
]
