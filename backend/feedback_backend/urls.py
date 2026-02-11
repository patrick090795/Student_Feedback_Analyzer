from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse


def index(request):
    return HttpResponse("<h1>Feedback Analyzer API</h1><p>Use POST /api/analyze/ to analyze comments.</p>")


urlpatterns = [
    path('', index),
    path('api/', include('api.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
