# Etape 1 : Build
FROM python:3.11-alpine AS builder

# Définition d'arguments
ARG APP_ENV=production

# Variables d'environnement
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    APP_ENV=${APP_ENV}

# Labels
LABEL maintainer="votre_nom <votre_email>" \
      version="1.0" \
      description="Image Flask optimisée"

WORKDIR /app

# Installation des dépendances système
RUN apk add --no-cache gcc musl-dev postgresql-dev

# Installation des dépendances Python
RUN pip install --no-cache-dir --upgrade pip
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Etape 2 : Image finale
FROM python:3.11-alpine

WORKDIR /app
ENV PATH=/root/.local/bin:$PATH

# Copie seulement ce qui est nécessaire
COPY --from=builder /root/.local /root/.local
COPY app app

EXPOSE 5000

# Commande de lancement (ici avec gunicorn pour la prod, par ex)
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app.main:app"]
