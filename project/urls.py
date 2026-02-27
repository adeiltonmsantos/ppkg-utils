from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin  # type: ignore
from django.urls import include, path  # type: ignore

urlpatterns = [
    path('admin/', admin.site.urls),
    path('documents/', include('appDocuments.urls'))
]

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)

urlpatterns += static(
    settings.STATIC_URL,
    document_root=settings.STATIC_ROOT
)
