from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Comment, Profile, SiteConfig


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if field_name == 'username':
                field.help_text = "Requis. 150 caractères ou moins. Lettres, chiffres et @/./+/-/_ uniquement."
            elif field_name == 'password1':
                field.help_text = "Votre mot de passe doit contenir au moins 8 caractères."
            elif field_name == 'password2':
                field.help_text = "Entrez le même mot de passe que précédemment."

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
            Profile.objects.create(user=user)
        return user

from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'media', 'video_url', 'media_type', 'is_published']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 8}),
            'media': forms.FileInput(attrs={'class': 'form-control'}),
            'video_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Collez ici l’URL YouTube si c’est une vidéo'
            }),
            'media_type': forms.Select(attrs={'class': 'form-select'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        media = cleaned_data.get('media')
        video_url = cleaned_data.get('video_url')

        if not media and not video_url:
            raise forms.ValidationError(
                "Vous devez fournir soit une image, soit une URL de vidéo."
            )
        if media and video_url:
            raise forms.ValidationError(
                "Veuillez fournir uniquement une image ou une URL vidéo, pas les deux."
            )

        return cleaned_data


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Écrivez votre commentaire...'
            }),
        }
        labels = {
            'content': 'Votre commentaire',
        }


class SiteConfigForm(forms.ModelForm):
    class Meta:
        model = SiteConfig
        fields = ['cv']
        widgets = {
            'cv': forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf,.doc,.docx'}),
        }
        labels = {
            'cv': 'Votre CV (PDF recommandé)'
        }