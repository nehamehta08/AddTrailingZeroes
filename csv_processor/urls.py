from django.urls import path
from . import views

urlpatterns = [
    path('process/', views.process_csv_view, name='process_csv'),
    path('download_processed_files/', views.download_all_processed_files, name='download_processed_files'),
]
