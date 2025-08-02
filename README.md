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
Créer un environnement virtuel et l’activer :

bash
Copier
Modifier
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows
Installer les dépendances :

bash
Copier
Modifier
pip install -r requirements.txt
Configurer la base de données (MySQL ou autre) dans settings.py.

Appliquer les migrations :

bash
Copier
Modifier
python manage.py migrate
Créer un super utilisateur (admin) :

bash
Copier
Modifier
python manage.py createsuperuser
Lancer le serveur de développement :

bash
Copier
Modifier
python manage.py runserver
Accéder à l’application sur : http://127.0.0.1:8000/

Utilisation
La page d’accueil affiche les derniers articles publiés.

La page blog liste tous les articles paginés avec barre de recherche.

Cliquer sur un article pour voir son détail, médias et commentaires.

Les utilisateurs peuvent s’inscrire, se connecter et poster des commentaires.

L’administrateur accède au tableau de bord via /admin-dashboard/ pour gérer articles et commentaires.

Technologies utilisées
Python 3.x

Django 4.x

Bootstrap 5

MySQL (ou autre base SQL)

HTML5 & CSS3

JavaScript (pour quelques interactions)

Contribution
Les contributions sont bienvenues !
Merci d’ouvrir une issue ou une pull request pour proposer des améliorations ou signaler un bug.

Licence
Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus d’informations.

Contact
Othmane Chaikhi - othmanechaikhi.pro@gmail.com

