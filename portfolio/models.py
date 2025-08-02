from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse


import os

class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name="Titre")
    content = models.TextField(verbose_name="Contenu")
    media = models.FileField(upload_to='posts_media/', blank=True, null=True, verbose_name="Média")

    MEDIA_TYPE_CHOICES = [
        ('image', 'Image'),
        ('video', 'Vidéo'),
    ]
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES, blank=True, null=True, verbose_name="Type de média")

    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Auteur")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Date de modification")
    is_published = models.BooleanField(default=True, verbose_name="Publié")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Article"
        verbose_name_plural = "Articles"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})

    @property
    def comment_count(self):
        return self.comments.filter(is_approved=True).count()

    def save(self, *args, **kwargs):
        if self.media:
            ext = os.path.splitext(self.media.name)[1].lower()
            if ext in ['.jpg', '.jpeg', '.png', '.gif']:
                self.media_type = 'image'
            elif ext in ['.mp4', '.avi', '.mov', '.webm']:
                self.media_type = 'video'
        super().save(*args, **kwargs)

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