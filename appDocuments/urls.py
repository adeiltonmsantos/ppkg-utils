from django.urls import path

from . import views

app_name = 'appDocuments'

urlpatterns = [
    path('home/', views.home, name='home'),
    path('ipem_data/', views.ipemData, name='ipem-data'),
]
