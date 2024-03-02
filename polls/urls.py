from django.contrib import admin
from django.urls import path,include
from polls import views

urlpatterns = [
    path('handle_pkl_upload/', views.handle_pkl_upload, name='handle_pkl_upload'),
    # path('handle_dropdown/', views.handle_dropdown, name='handle_dropdown'),
    path('process_parameter_form/', views.process_parameter_form, name='process_parameter_form'),
    path('admin/', admin.site.urls),
    path('get_csrf_token/', views.get_csrf_token, name="get_csrf_token"),
    path('', views.index, name='index')
]