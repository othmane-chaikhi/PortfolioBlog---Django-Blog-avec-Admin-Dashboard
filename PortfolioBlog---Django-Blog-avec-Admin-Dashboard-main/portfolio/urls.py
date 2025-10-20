from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Pages publiques
    path('', views.home, name='home'),
    path('blog/', views.blog, name='blog'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    
    # Authentification
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Dashboard admin
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-dashboard/settings/cv/', views.admin_cv_settings, name='admin_cv_settings'),
    path('download-cv/', views.download_cv, name='download_cv'),
    
    # Gestion des posts
    path('admin-dashboard/posts/', views.admin_posts, name='admin_posts'),
    path('admin-dashboard/posts/create/', views.admin_post_create, name='admin_post_create'),
    path('admin-dashboard/posts/<int:pk>/edit/', views.admin_post_edit, name='admin_post_edit'),
    path('admin-dashboard/posts/<int:pk>/delete/', views.admin_post_delete, name='admin_post_delete'),
    
    # Gestion des commentaires
    path('admin-dashboard/comments/', views.admin_comments, name='admin_comments'),
    path('admin-dashboard/comments/<int:pk>/toggle/', views.admin_comment_toggle, name='admin_comment_toggle'),
    path('admin-dashboard/comments/<int:pk>/delete/', views.admin_comment_delete, name='admin_comment_delete'),
]