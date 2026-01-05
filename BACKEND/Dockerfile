# Utilise une image officielle Python 3.13 slim
FROM python:3.13-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier le requirements.txt
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier tout le projet dans le conteneur
COPY . .

# Définir la variable d'environnement pour Flask
ENV FLASK_APP=run.py
ENV FLASK_RUN_HOST=0.0.0.0

#ENV FLASK_ENV=development
ENV FLASK_ENV=production


# Exposer le port utilisé par Flask
EXPOSE 5000

# Commande pour lancer Flask
#CMD ["python", "run.py"]
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "5", "run:app"]
