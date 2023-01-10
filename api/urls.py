from django.urls import path
from . import views

urlpatterns = [
    path('bucket/create', views.CreateBucket.as_view(), name='create_bucket'),
    path('bucket/list', views.ListBuckets.as_view(), name='list_buckets'),
    path('bucket/check', views.CheckBucket.as_view(), name='check_bucket'),
    path('bucket/delete', views.DeleteBucket.as_view(), name='delete_bucket'),
    # path('create-bucket/', views.create_bucket, name='create_bucket'),
    # path('upload/', views.FileUploadView.as_view(), name='upload'),
    path('file/upload', views.UploadFile.as_view(), name='upload_file'),
    path('file/list', views.ListFiles.as_view(), name='list_files'),
    path('file/delete', views.DeleteFile.as_view(), name='delete_file'),
    path('file/download', views.FileDownload.as_view(), name='download_file'),
]

