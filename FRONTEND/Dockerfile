# Étape unique : utiliser directement Nginx
FROM nginx:alpine

# Copier la version buildée de l'app
COPY dist/ /usr/share/nginx/html

# Remplacer la config
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Exposer le port HTTP standard
EXPOSE 80
