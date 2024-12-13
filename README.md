# Docker Swarm Multi-Service Stack

## 📄 Description

Ce projet implémente une architecture multi-services utilisant **Docker Swarm** pour l'orchestration. Il comprend les composants suivants :

-   **Flask** : Application web légère en Python.
-   **PostgreSQL** : Base de données relationnelle.
-   **Nginx** : Serveur web pour gérer les requêtes HTTP et agir comme proxy inverse.
-   **Portainer** _(optionnel)_ : Interface web pour gérer visuellement tes conteneurs Docker.

Cette stack est conçue pour être scalable, sécurisée et facile à déployer, offrant une solution robuste pour les applications web modernes.

## 📚 Table des Matières

-   [Docker Swarm Multi-Service Stack](#docker-swarm-multi-service-stack)
    -   [📄 Description](#-description)
    -   [📚 Table des Matières](#-table-des-matières)
    -   [🔧 Prérequis](#-prérequis)
    -   [🛠️ Installation](#️-installation)
        -   [1. Cloner le Répertoire du Projet](#1-cloner-le-répertoire-du-projet)
        -   [2. Construire l'Image Flask](#2-construire-limage-flask)
        -   [3. Vérifier les Images Disponibles](#3-vérifier-les-images-disponibles)
    -   [🛠️ Configuration](#️-configuration)
        -   [Secrets](#secrets)
            -   [1. Créer les Fichiers de Secrets](#1-créer-les-fichiers-de-secrets)
            -   [2. Vérifier les Secrets](#2-vérifier-les-secrets)
        -   [Configuration de Nginx](#configuration-de-nginx)
            -   [Exemple de `nginx.conf`](#exemple-de-nginxconf)
    -   [🛠️ Construction de l'Image Flask](#️-construction-de-limage-flask)
        -   [Étapes pour Construire l'Image Flask](#étapes-pour-construire-limage-flask)
    -   [🛠️ Déploiement de la Stack Docker Swarm](#️-déploiement-de-la-stack-docker-swarm)
        -   [Initialiser Docker Swarm](#initialiser-docker-swarm)
        -   [Déployer la Stack](#déployer-la-stack)
        -   [Vérifier les Services Déployés](#vérifier-les-services-déployés)
    -   [🚀 Utilisation](#-utilisation)
        -   [Accéder à l'Application](#accéder-à-lapplication)
        -   [Tester avec `curl`](#tester-avec-curl)
    -   [🛠️ Gestion des Services](#️-gestion-des-services)
        -   [Vérifier l'État des Services](#vérifier-létat-des-services)
        -   [Vérifier les Tâches des Services](#vérifier-les-tâches-des-services)
        -   [Mettre à Jour un Service](#mettre-à-jour-un-service)
    -   [📈 Surveillance avec Portainer (Optionnel)](#-surveillance-avec-portainer-optionnel)
        -   [Installation de Portainer](#installation-de-portainer)
        -   [Accéder à Portainer](#accéder-à-portainer)
    -   [🔒 Gestion des Secrets](#-gestion-des-secrets)
        -   [Ajouter un Secret](#ajouter-un-secret)
        -   [Liste des Secrets](#liste-des-secrets)
        -   [Afficher un Secret](#afficher-un-secret)
    -   [🧪 Tests](#-tests)
        -   [Tester les Services Individuellement](#tester-les-services-individuellement)
            -   [1. Tester Flask](#1-tester-flask)
            -   [2. Tester PostgreSQL](#2-tester-postgresql)
        -   [Vérifier les Logs](#vérifier-les-logs)

## 🔧 Prérequis

Avant de commencer, assure-toi d'avoir installé les éléments suivants :

-   [Docker](https://docs.docker.com/get-docker/) (version 20.10 ou supérieure)
-   [Docker Compose](https://docs.docker.com/compose/install/) (version 1.27.0 ou supérieure)
-   [Git](https://git-scm.com/downloads)
-   Accès à Docker Swarm (initialisé sur ta machine)

## 🛠️ Installation

### 1. Cloner le Répertoire du Projet

Commence par cloner le dépôt GitHub et navigue dans le répertoire du projet.

```bash
git clone https://github.com/votre-utilisateur/docker-swarm-multi-service.git
cd docker-swarm-multi-service/docker
```

### 2. Construire l'Image Flask

Docker Swarm ignore l'option `build` dans le fichier `docker-compose.yml`. Tu dois donc construire l'image Flask manuellement.

```bash
cd ./flask
docker build -t docker-flask:latest .
cd ..
```

### 3. Vérifier les Images Disponibles

Assure-toi que l'image Flask a été construite correctement.

```bash
docker images
```

Tu devrais voir `docker-flask:latest` dans la liste des images.

## 🛠️ Configuration

### Secrets

Les secrets Docker sont utilisés pour gérer les informations sensibles comme les mots de passe. Ils sont définis dans le fichier `docker-compose.yml` et stockés de manière sécurisée.

#### 1. Créer les Fichiers de Secrets

Crée un répertoire `secrets` à la racine du dossier `docker` si ce n'est pas déjà fait, et ajoute les fichiers suivants :

-   **`secrets/db_user.txt`**

    ```
    postgres
    ```

-   **`secrets/db_password.txt`**

    ```
    mysecretpassword
    ```

#### 2. Vérifier les Secrets

Tu peux lister les secrets créés :

```bash
docker secret ls
```

### Configuration de Nginx

Assure-toi que le fichier `nginx/nginx.conf` est configuré correctement pour proxy les requêtes vers le service Flask.

#### Exemple de `nginx.conf`

```nginx
server {
    listen 80;

    location / {
        proxy_pass http://flask:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 🛠️ Construction de l'Image Flask

Comme Docker Swarm ne supporte pas l'option `build` dans `docker-compose.yml`, tu dois construire l'image Flask manuellement.

### Étapes pour Construire l'Image Flask

1. **Naviguer vers le Répertoire Flask :**

    ```bash
    cd ./flask
    ```

2. **Construire l'Image Flask :**

    ```bash
    docker build -t docker-flask:latest .
    ```

3. **Retourner au Répertoire Principal :**

    ```bash
    cd ..
    ```

## 🛠️ Déploiement de la Stack Docker Swarm

### Initialiser Docker Swarm

Si Docker Swarm n'est pas encore initialisé sur ta machine, tu peux l'initialiser avec la commande suivante :

```bash
docker swarm init
```

### Déployer la Stack

Déploie ta stack Docker Swarm avec le fichier `docker-compose.yml` corrigé :

```bash
docker stack deploy --compose-file docker-compose.yml my_stack
```

**Remarque :** Docker Swarm ignore les options `build` dans `docker-compose.yml`. Assure-toi d'avoir construit toutes les images nécessaires manuellement avant le déploiement.

### Vérifier les Services Déployés

Après le déploiement, vérifie que tous les services sont en état `Running` :

```bash
docker stack services my_stack
```

**Sortie Attendue :**

```
ID             NAME                MODE         REPLICAS   IMAGE                 PORTS
jmycpzddjctn   my_stack_flask      replicated   2/2        docker-flask:latest
4gtca36p7mcr   my_stack_nginx      replicated   2/2        nginx:alpine          *:80->80/tcp
yyp08rezdc45   my_stack_postgres   replicated   1/1        postgres:15-alpine
```

## 🚀 Utilisation

### Accéder à l'Application

Ouvre ton navigateur et va à :

```
http://localhost
```

Tu devrais voir la réponse JSON suivante :

```json
{ "message": "Hello from Flask with DB connection OK!" }
```

### Tester avec `curl`

Depuis ta machine hôte, tu peux également tester avec :

```bash
curl http://localhost
```

**Sortie Attendue :**

```json
{ "message": "Hello from Flask with DB connection OK!" }
```

## 🛠️ Gestion des Services

### Vérifier l'État des Services

Pour vérifier l'état des services déployés :

```bash
docker stack services my_stack
```

### Vérifier les Tâches des Services

Assure-toi que les tâches de chaque service sont en état `Running` :

```bash
docker service ps my_stack_nginx
```

**Sortie Attendue :**

```
ID             NAME               IMAGE          NODE             DESIRED STATE   CURRENT STATE            ERROR     PORTS
as7q4x142w6m   my_stack_nginx.1   nginx:alpine   docker-desktop   Running         Running 10 seconds ago
veupz8fpi0c1   my_stack_nginx.2   nginx:alpine   docker-desktop   Running         Running 10 seconds ago
```

### Mettre à Jour un Service

Pour mettre à jour le nombre de répliques d'un service (par exemple, Flask) :

```bash
docker service update --replicas 3 my_stack_flask
```

## 📈 Surveillance avec Portainer (Optionnel)

**Portainer** est une interface web pour gérer visuellement tes conteneurs Docker, stacks et services Swarm.

### Installation de Portainer

Sous Docker Desktop sur Windows, utilise des chemins de style Unix pour les volumes.

```bash
docker run -d -p 9000:9000 --name portainer   --restart=always   -v //var/run/docker.sock:/var/run/docker.sock   portainer/portainer-ce
```

### Accéder à Portainer

1. Ouvre ton navigateur et va à :

    ````
    http://localhost:9000
    ```

    ````

2. Suis les instructions pour configurer ton compte administrateur.

3. Connecte-toi et commence à gérer tes services Docker Swarm via l'interface web de Portainer.

## 🔒 Gestion des Secrets

### Ajouter un Secret

Pour ajouter un nouveau secret :

1. Crée un fichier contenant le secret, par exemple `secrets/new_secret.txt`.
2. Ajoute-le au fichier `docker-compose.yml` sous la section `secrets`.

### Liste des Secrets

Pour lister tous les secrets :

```bash
docker secret ls
```

### Afficher un Secret

Pour afficher le contenu d'un secret :

```bash
docker secret inspect my_stack_db_password --pretty
```

**Note :** Les secrets sont stockés de manière sécurisée et ne peuvent pas être affichés en clair.

## 🧪 Tests

### Tester les Services Individuellement

#### 1. Tester Flask

Accède directement au service Flask depuis un conteneur ou ta machine hôte.

```bash
curl http://localhost:5000
```

**Sortie Attendue :**

```json
{ "message": "Hello from Flask with DB connection OK!" }
```

#### 2. Tester PostgreSQL

Connecte-toi à PostgreSQL pour vérifier l'état de la base de données.

```bash
docker exec -it $(docker ps -qf "name=my_stack_postgres") psql -U postgres -d mydb -c '\du'
```

**Sortie Attendue :**

```
                                           List of roles
  Role name |                         Attributes                         | Member of
-----------+------------------------------------------------------------+-----------
 postgres  | Superuser, Create role, Create DB, Replication, Bypass RLS | {}
```

### Vérifier les Logs

Consulte les logs pour détecter d'éventuelles erreurs ou confirmer le bon fonctionnement.

```bash
docker service logs my_stack_flask
docker service logs my_stack_nginx
docker service logs my_stack_postgres
```
