from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Post  # موديل المقالات (عدّل الاسم إذا كان مختلف)

class StaticViewSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.6

    def items(self):
        # أسماء الـ URL patterns التي لها name في urls.py
        return ['home', 'blog']

    def location(self, item):
        return reverse(item)

class PostSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8  # أعلى من الصفحات الثابتة
    def items(self):
        return Post.objects.all()

    def lastmod(self, obj):
        # تعديل آخر مرة تم تعديل البوست
        return obj.updated_at  # تأكد أن عندك الحقل updated_at في الموديل
