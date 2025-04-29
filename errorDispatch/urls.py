from django.urls import path  # type: ignore

from errorDispatch.views import loadReport

urlpatterns = [
    path('despacho/laudo', loadReport)
]
