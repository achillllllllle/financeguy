# Stage de build
FROM node:18-alpine as build-front

WORKDIR /app

# Copier les fichiers de dépendances
COPY package*.json ./

# Installer les dépendances
RUN npm ci

# Copier le code source
COPY . .

# Build l'application
RUN npm run build

# Stage de développement
FROM node:18-alpine as dev-front

WORKDIR /app

# Copier les fichiers de dépendances
COPY package*.json ./

# Installer les dépendances
RUN npm ci

# Copier le code source
COPY . .

# Exposer le port
EXPOSE 8080

# Commande pour le développement
CMD ["npm", "run", "serve"]

# Stage de production
FROM nginx:stable-alpine as run-front

# Copier la configuration nginx
COPY --from=build-front /app/dist /usr/share/nginx/html

# Copier la configuration nginx personnalisée
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
