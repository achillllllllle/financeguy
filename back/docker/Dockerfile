# Stage de build
FROM python:3.10-slim as build-back

WORKDIR /app

# Copier uniquement les fichiers nécessaires pour l'installation des dépendances
COPY requirements.txt .

# Installer les dépendances dans un répertoire virtuel
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir -r requirements.txt

# Stage final
FROM python:3.10-slim as run-back

WORKDIR /app

# Copier l'environnement virtuel depuis le stage de build
COPY --from=build-back /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copier le code source
COPY . .

# Variables d'environnement
ENV FLASK_APP=app.py
ENV FLASK_ENV=development

# Exposer le port
EXPOSE 5000

# Commande pour exécuter l'application
CMD ["flask", "run", "--host=0.0.0.0"]
