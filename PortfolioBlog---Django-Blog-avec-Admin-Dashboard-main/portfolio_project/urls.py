from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.contrib.sitemaps.views import sitemap
from portfolio.sitemaps import StaticViewSitemap, PostSitemap  # استيراد السايت ماب الجديد

sitemaps = {
    'static': StaticViewSitemap,
    'posts': PostSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('portfolio.urls')),

    # robots.txt
    path('robots.txt', TemplateView.as_view(
        template_name="robots.txt", content_type='text/plain'
    )),

    # sitemap.xml
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django-sitemap'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
