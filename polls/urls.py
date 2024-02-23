from django.contrib import admin
from django.urls import path,include
from polls import views

urlpatterns = [
    path('handle_csv_upload/', views.handle_csv_upload, name='handle_csv_upload'),
    path('admin/', admin.site.urls),
    path('', views.index, name='index')
]
