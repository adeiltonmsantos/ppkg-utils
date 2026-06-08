from django.urls import path  # type: ignore

from . import views

app_name = 'appDocuments'

urlpatterns = [
    path(
        'ipem_data/',
        views.IpemData.as_view(),
        name='ipem-data-send'
    ),
    path(
        'ipem_data/receive/',
        views.IpemData.as_view(),
        name='ipem-data-receive'
    ),
    path(
        'high-error-dispatch',
        views.HighErrorDispatch.as_view(),
        name='high-error-dispatch'
    ),
    path(
        'upload-exam-schedule',
        views.UploadExamSchedule.as_view(),
        name='upload-exam-schedule'
    ),
    path(
        'edit-exam-schedule',
        views.EditExamSchedule.as_view(),
        name='edit-exam-schedule'
    ),
]
