# PortfolioBlog - Django Blog avec Admin Dashboard

Une application web Django permettant de gérer un blog personnel avec un tableau de bord administrateur complet.  
Idéal pour un portfolio personnel ou un blog professionnel avec gestion simplifiée des contenus et commentaires.

---

## Fonctionnalités

- Création, modification et suppression d'articles (support image et vidéo)  
- Gestion des commentaires avec modération (approbation/suppression)  
- Authentification des utilisateurs avec rôles :  
  - Administrateur (accès au dashboard)  
  - Utilisateur simple (lecture, commentaires)  
- Pages publiques :  
  - Accueil avec articles récents  
  - Liste des articles paginée (blog)  
  - Détail d’article avec médias et commentaires  
- Interface responsive avec Bootstrap 5  
- Notifications via messages Django  
- Téléchargement et affichage médias (image/vidéo) depuis le serveur

---

## Installation

1. Cloner le dépôt :
   ```bash
   git clone https://github.com/ton-utilisateur/PortfolioBlog.git
   cd PortfolioBlog
