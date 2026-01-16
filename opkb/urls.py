"""
URL configuration for opkb project.
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from knowledge import views as knowledge_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin/stats/', knowledge_views.admin_stats_view, name='admin_stats'),
    path('api/', include('knowledge.urls')),
    # Catch-all pour SPA React
    re_path(r'^(?!api|admin|static|media).*$', TemplateView.as_view(template_name='index.html')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

