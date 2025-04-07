# FinanceGuy

Application de gestion financière personnelle avec backend Flask et frontend Vue.js.

## Configuration

1. Copiez le fichier `.env.example` en `.env` :
```bash
cp .env.example .env
```

2. Modifiez le fichier `.env` avec vos valeurs :
```env
POSTGRES_USER=your_db_user
POSTGRES_PASSWORD=your_db_password
POSTGRES_DB=your_db_name
JWT_SECRET_KEY=your_jwt_secret_key
```

## Démarrage avec Docker Compose

1. Construisez et démarrez les conteneurs :
```bash
docker-compose up --build
```

2. Accédez à l'application :
- Frontend : http://localhost:5173
- Backend API : http://localhost:5000/api/v1

## Structure du projet

- `back/` : Backend Flask
  - `app/` : Code source de l'application
  - `requirements.txt` : Dépendances Python
  - `Dockerfile` : Configuration Docker

- `front/` : Frontend Vue.js
  - `src/` : Code source de l'application
  - `package.json` : Dépendances Node.js
  - `Dockerfile` : Configuration Docker

## Sécurité

- Les informations sensibles sont stockées dans des variables d'environnement
- Le fichier `.env` est ignoré par Git
- Utilisez des mots de passe forts pour la base de données et la clé JWT 