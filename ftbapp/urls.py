from django.urls import path
from . import views

urlpatterns = [
    path('upload-song/', views.UploadSongView.as_view(), name='upload-song'),
    path('bars/<path:file_path>/', views.bars, name='bars'),
    path('vibrations/<path:file_path>/', views.vibrations, name='vibrations'),
    path('colors/<path:file_path>/', views.colors, name='colors'),
]