import os
import tempfile
from io import BytesIO
from PIL import Image

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.core.files.base import ContentFile


class Post(models.Model):
    MEDIA_TYPE_CHOICES = [
        ('image', 'Image'),
        ('video', 'Vidéo'),
    ]

    title = models.CharField(max_length=200, verbose_name="Titre")
    content = models.TextField(verbose_name="Contenu")
    media = models.FileField(upload_to='posts_media/', blank=True, null=True, verbose_name="Média")  # keep for images
    video_url = models.URLField(blank=True, null=True, verbose_name="URL Vidéo")  # new field for YouTube links
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES, blank=True, null=True, verbose_name="Type de média")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Auteur")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Date de modification")
    is_published = models.BooleanField(default=True, verbose_name="Publié")

    def save(self, *args, **kwargs):
        if self.media:
            ext = os.path.splitext(self.media.name)[1].lower()
            if ext in ['.jpg', '.jpeg', '.png', '.gif']:
                self.media_type = 'image'
                self.media = self.compress_image(self.media)
        elif self.video_url:
            self.media_type = 'video'
        super().save(*args, **kwargs)

    def compress_image(self, uploaded_file):
        """Compress uploaded images (JPEG/PNG) and keep GIFs unchanged.
        Returns a ContentFile with the same or adjusted filename.
        """
        try:
            ext = os.path.splitext(uploaded_file.name)[1].lower()
            if ext == '.gif':
                return uploaded_file

            img = Image.open(uploaded_file)

            # Resize to a reasonable max dimension while keeping aspect ratio
            max_size = (1600, 1600)
            img.thumbnail(max_size, Image.LANCZOS)

            buffer = BytesIO()

            if ext in ['.jpg', '.jpeg']:
                if img.mode in ('RGBA', 'P'):
                    img = img.convert('RGB')
                img.save(buffer, format='JPEG', quality=75, optimize=True)
                new_name = os.path.splitext(uploaded_file.name)[0] + '.jpg'
            elif ext == '.png':
                # Keep PNG to preserve transparency
                img.save(buffer, format='PNG', optimize=True)
                new_name = uploaded_file.name
            else:
                # Unsupported types: return as-is
                return uploaded_file

            buffer.seek(0)
            return ContentFile(buffer.getvalue(), name=new_name)
        except Exception:
            # On any error, fallback to original file
            return uploaded_file


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name="Article")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Auteur")
    content = models.TextField(verbose_name="Commentaire")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Date de création")
    is_approved = models.BooleanField(default=True, verbose_name="Approuvé")

    class Meta:
        ordering = ['created_at']
        verbose_name = "Commentaire"
        verbose_name_plural = "Commentaires"

    def __str__(self):
        return f'Commentaire de {self.author.username} sur {self.post.title}'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True, verbose_name="Biographie")
    location = models.CharField(max_length=30, blank=True, verbose_name="Localisation")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Date de naissance")
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name="Avatar")

    class Meta:
        verbose_name = "Profil"
        verbose_name_plural = "Profils"

    def __str__(self):
        return f'Profil de {self.user.username}'


class SiteConfig(models.Model):
    cv = models.FileField(upload_to='cv/', blank=True, null=True, verbose_name="CV (PDF)")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Configuration du site"
        verbose_name_plural = "Configuration du site"

    def __str__(self):
        return "Configuration du site"

    @classmethod
    def get_solo(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj
