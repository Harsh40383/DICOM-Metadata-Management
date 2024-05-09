# dicom/urls.py

from django.urls import path
from . import views

urlpatterns = [  
    path('', views.show, name="show"),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('upload/', views.upload_dicom, name='upload_dicom'),
    path('q', views.search_list, name="searchdata"),
]
