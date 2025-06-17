# 🧰 SoftDesk - API Back-End

Bienvenue sur le back-end de l'application **SoftDesk Support**, une API RESTful permettant de créer et suivre des projets, 
tâches et commentaires pour des équipes de développement. Ce projet est réalisé avec **Django** et **Django REST Framework**.

## 📁 Structure du projet
softdesk/
│
├── authentication/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── ...
│
├── softdesk/
│   ├── settings.py
│   ├── urls.py
│   └── ...
│
├── Pipfile
├── Pipfile.lock
└── manage.py

---


## ⚙️ Technologies

- Python 3.12.6
- Django 4+
- Django REST Framework
- Authentification JWT (via `djangorestframework-simplejwt`)
- Pipenv (gestionnaire de dépendances)

---

## 🚀 Installation locale

### 1. Cloner le dépôt
```bash
git clone https://github.com/votre-utilisateur/softdesk-backend.git
cd softdesk-backend 

### 2. Installer les dépendances avec Pipenv
```bash
pipenv install --python 3.12.6
pipenv install django djangorestframework djangorestframework-simplejwt

### 3. Appliquer les migrations
```bash
pipenv run python manage.py makemigrations
pipenv run python manage.py migrate

### 4. Démarrer le serveur
```bash
pipenv run python manage.py runserver

## Le serveur tourne ensuite à : http://127.0.0.1:8000/
