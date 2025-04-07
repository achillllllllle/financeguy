# Financeguy Backend

Backend de l'application Financeguy, une application de gestion de finances personnelles.

## Prérequis

- Python 3.8+
- PostgreSQL
- pip (gestionnaire de paquets Python)

## Installation

1. Cloner le repository :
```bash
git clone <url-du-repo>
cd financeguy/back
```

2. Créer un environnement virtuel et l'activer :
```bash
python -m venv venv
source venv/bin/activate  # Sur Windows : venv\Scripts\activate
```

3. Installer les dépendances :
```bash
pip install -r requirements.txt
```

4. Configurer les variables d'environnement :
- Copier le fichier `.env.example` vers `.env`
- Modifier les variables dans `.env` selon votre configuration

5. Créer la base de données PostgreSQL :
```bash
createdb financeguy
```

## Lancement de l'application

Pour lancer l'application en mode développement :
```bash
uvicorn app.main:app --reload
```

L'API sera accessible à l'adresse : http://localhost:8000

## Documentation de l'API

La documentation interactive de l'API est disponible à :
- Swagger UI : http://localhost:8000/docs
- ReDoc : http://localhost:8000/redoc

## Endpoints disponibles

### Authentification
- POST `/api/v1/token` - Connexion et obtention du token JWT
- POST `/api/v1/users/` - Création d'un nouvel utilisateur

### Transactions
- POST `/api/v1/transactions/` - Création d'une nouvelle transaction
- GET `/api/v1/transactions/` - Liste des transactions
- GET `/api/v1/balance/` - Consultation du solde

### Rappels
- POST `/api/v1/reminders/` - Création d'un nouveau rappel
- GET `/api/v1/reminders/` - Liste des rappels
- PUT `/api/v1/reminders/{reminder_id}/` - Modification d'un rappel
- DELETE `/api/v1/reminders/{reminder_id}/` - Suppression d'un rappel

## Tests

Pour lancer les tests :
```bash
pytest
``` 