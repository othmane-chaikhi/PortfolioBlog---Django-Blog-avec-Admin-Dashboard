from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from urllib.parse import urlparse, parse_qs

from .models import Post, Comment, SiteConfig
from .forms import CustomUserCreationForm, PostForm, CommentForm, SiteConfigForm


def get_embed_url(video_url):
    """Transforme une URL YouTube en URL embed valide"""
    if not video_url:
        return None
    parsed_url = urlparse(video_url)
    if parsed_url.hostname in ['www.youtube.com', 'youtube.com']:
        query = parse_qs(parsed_url.query)
        video_id = query.get('v')
        if video_id:
            return f"https://www.youtube.com/embed/{video_id[0]}"
    elif parsed_url.hostname == 'youtu.be':
        video_id = parsed_url.path[1:]
        return f"https://www.youtube.com/embed/{video_id}"
    return None


def home(request):
    """Page d'accueil avec les derniers posts"""
    recent_posts = Post.objects.filter(is_published=True)[:3]

    # Préparer l'URL embed pour les vidéos YouTube
    for post in recent_posts:
        post.video_embed_url = get_embed_url(post.video_url)

    context = {
        'recent_posts': recent_posts,
        'page_title': 'Accueil'
    }
    return render(request, 'portfolio/home.html', context)


def blog(request):
    """Page blog avec tous les posts"""
    search_query = request.GET.get('search', '')
    posts = Post.objects.filter(is_published=True)

    if search_query:
        posts = posts.filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query)
        )

    # Préparer l'URL embed pour les vidéos YouTube
    for post in posts:
        post.video_embed_url = get_embed_url(post.video_url)

    paginator = Paginator(posts, 6)  # 6 posts par page
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)

    context = {
        'posts': posts,
        'search_query': search_query,
        'page_title': 'Blog'
    }
    return render(request, 'portfolio/blog.html', context)


def post_detail(request, pk):
    """Détail d'un post avec commentaires"""
    post = get_object_or_404(Post, pk=pk, is_published=True)
    comments = post.comments.filter(is_approved=True)

    # Préparer l'URL embed pour les vidéos YouTube
    post.video_embed_url = get_embed_url(post.video_url)

    if request.method == 'POST' and request.user.is_authenticated:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Votre commentaire a été ajouté avec succès!')
            return redirect('post_detail', pk=pk)
    else:
        form = CommentForm()

    context = {
        'post': post,
        'comments': comments,
        'form': form,
        'page_title': post.title
    }
    return render(request, 'portfolio/post_detail.html', context)


def register(request):
    """Inscription utilisateur"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Compte créé avec succès! Vous êtes maintenant connecté.')
            return redirect('home')
    else:
        form = CustomUserCreationForm()

    context = {
        'form': form,
        'page_title': 'Inscription'
    }
    return render(request, 'registration/register.html', context)


@staff_member_required
def admin_dashboard(request):
    """Dashboard administrateur"""
    posts = Post.objects.all()[:5]
    recent_comments = Comment.objects.all()[:5]

    stats = {
        'total_posts': Post.objects.count(),
        'published_posts': Post.objects.filter(is_published=True).count(),
        'total_comments': Comment.objects.count(),
        'pending_comments': Comment.objects.filter(is_approved=False).count(),
    }

    context = {
        'posts': posts,
        'recent_comments': recent_comments,
        'stats': stats,
        'page_title': 'Dashboard Admin'
    }
    return render(request, 'portfolio/admin/dashboard.html', context)


@staff_member_required
def admin_cv_settings(request):
    """Gérer le CV (upload/remplacement)"""
    config = SiteConfig.get_solo()
    if request.method == 'POST':
        form = SiteConfigForm(request.POST, request.FILES, instance=config)
        if form.is_valid():
            form.save()
            messages.success(request, 'CV mis à jour avec succès!')
            return redirect('admin_cv_settings')
    else:
        form = SiteConfigForm(instance=config)

    context = {
        'form': form,
        'config': config,
        'page_title': 'Gérer mon CV'
    }
    return render(request, 'portfolio/admin/cv_settings.html', context)


def download_cv(request):
    """Redirige vers l'URL du CV ou informe si indisponible"""
    config = SiteConfig.get_solo()
    if config.cv:
        return redirect(config.cv.url)
    messages.warning(request, 'Le CV n\'est pas encore disponible.')
    return redirect('home')


@staff_member_required
def admin_posts(request):
    """Liste des posts pour l'admin"""
    posts = Post.objects.all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)

    context = {
        'posts': posts,
        'page_title': 'Gestion des Articles'
    }
    return render(request, 'portfolio/admin/posts.html', context)


@staff_member_required
def admin_post_create(request):
    """Créer un nouveau post"""
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Article créé avec succès!')
            return redirect('admin_posts')
    else:
        form = PostForm()

    context = {
        'form': form,
        'post': None,
        'page_title': 'Créer un Article'
    }
    return render(request, 'portfolio/admin/post_form.html', context)


@staff_member_required
def admin_post_edit(request, pk):
    """Modifier un post existant"""
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Article modifié avec succès!')
            return redirect('admin_posts')
    else:
        form = PostForm(instance=post)

    context = {
        'form': form,
        'post': post,
        'page_title': 'Modifier l\'Article'
    }
    return render(request, 'portfolio/admin/post_form.html', context)


@staff_member_required
def admin_post_delete(request, pk):
    """Supprimer un post"""
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Article supprimé avec succès!')
        return redirect('admin_posts')

    context = {
        'post': post,
        'page_title': 'Supprimer l\'Article'
    }
    return render(request, 'portfolio/admin/post_confirm_delete.html', context)


@staff_member_required
def admin_comments(request):
    """Gestion des commentaires"""
    comments = Comment.objects.all()
    paginator = Paginator(comments, 20)
    page_number = request.GET.get('page')
    comments = paginator.get_page(page_number)

    context = {
        'comments': comments,
        'page_title': 'Gestion des Commentaires'
    }
    return render(request, 'portfolio/admin/comments.html', context)


@staff_member_required
def admin_comment_toggle(request, pk):
    """Approuver/désapprouver un commentaire"""
    comment = get_object_or_404(Comment, pk=pk)
    comment.is_approved = not comment.is_approved
    comment.save()

    status = "approuvé" if comment.is_approved else "désapprouvé"
    messages.success(request, f'Commentaire {status} avec succès!')
    return redirect('admin_comments')


@staff_member_required
def admin_comment_delete(request, pk):
    """Supprimer un commentaire"""
    comment = get_object_or_404(Comment, pk=pk)

    if request.method == 'POST':
        comment.delete()
        messages.success(request, 'Commentaire supprimé avec succès!')
        return redirect('admin_comments')

    context = {
        'comment': comment,
        'page_title': 'Supprimer le Commentaire'
    }
    return render(request, 'portfolio/admin/comment_confirm_delete.html', context)
