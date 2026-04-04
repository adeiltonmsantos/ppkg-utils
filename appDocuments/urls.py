from django.urls import path  # type: ignore

from . import views

app_name = 'appDocuments'

urlpatterns = [
    path('home/', views.all.home, name='home'),
    path(
        'ipem_data/',
        views.IpemData.as_view(),
        name='ipem-data-send'
    ),
    path(
        'ipem_data/receive',
        views.IpemData.as_view(),
        name='ipem-data-receive'
    ),
]
