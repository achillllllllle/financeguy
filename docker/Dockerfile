# Utiliser une image Python officielle comme base
FROM python:3.10-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier les fichiers nécessaires dans le conteneur
COPY . /app

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Exposer le port 5000 (utilisé par Flask)
EXPOSE 5000

# Commande par défaut pour exécuter l'application
CMD ["flask", "run", "--host=0.0.0.0"]
