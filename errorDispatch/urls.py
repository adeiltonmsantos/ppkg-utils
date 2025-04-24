from django.urls import path  # type: ignore

from errorDispatch.views import loadReport

url_patterns = [
    path('laudo', loadReport)
]
