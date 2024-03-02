from django.contrib import admin
from django.urls import path,include
from polls import views

urlpatterns = [
    path('handle_csv_upload/', views.handle_pkl_upload, name='handle_csv_upload'),
    # path('handle_dropdown/', views.handle_dropdown, name='handle_dropdown'),
    path('process_parameter_form/', views.process_parameter_form, name='process_parameter_form'),
    path('admin/', admin.site.urls),
    path('', views.index, name='index')
]