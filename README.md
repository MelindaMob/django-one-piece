# One Piece Knowledge Base (OPKB)

**Projet B3 - Base de connaissances sur l'univers One Piece**

**Auteur:** [NOM] [PRENOM]  
**Sujet:** Application web de type "base de connaissances" sur l'univers One Piece

## 📋 Description

OPKB est une application web complète permettant de consulter et gérer une base de données sur l'univers One Piece. Le projet comprend :

- **Back-office Django Admin** : CRUD complet, exports (PDF, CSV, JSON), statistiques avec graphiques
- **API REST Django Rest Framework** : API en lecture seule (GET uniquement) avec pagination, recherche et tri
- **Frontend React + Vite** : Interface utilisateur moderne pour consulter les données avec navigation entre entités
- **Base de données Oracle** : Via Docker avec gvenzl/oracle-xe

## 🏗️ Architecture

### Stack technique

- **Backend:** Django 4.2.7 + Django Rest Framework 3.14.0
- **Base de données:** Oracle XE (via Docker)
- **Frontend:** React 18 + Vite 5
- **Outils:** ReportLab (PDF), Matplotlib (graphiques), Faker (génération de données)

### Structure du projet

```
django-projet-op/
├── opkb/                    # Configuration Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── knowledge/               # Application principale
│   ├── models.py            # Modèles (Character, Crew, Arc, Episode, DevilFruit, FruitHolder)
│   ├── admin.py             # Admin avec exports PDF/CSV, graphiques
│   ├── serializers.py       # Serializers DRF
│   ├── views.py             # ViewSets DRF + vue stats
│   ├── urls.py              # Routes API
│   └── management/
│       └── commands/
│           ├── seed_onepiece.py  # Génération de données
│           └── export_json.py    # Export JSON
├── frontend/                # Application React
│   ├── src/
│   │   ├── App.jsx
│   │   ├── pages/           # Pages React
│   │   └── ...
│   ├── package.json
│   └── vite.config.js
├── templates/               # Templates Django
│   ├── index.html          # Template SPA React
│   └── admin/
│       └── stats.html       # Page stats admin
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

## 🗄️ Modèles de données

### Table principale: Character (≥7 champs)
- `name` (CharField, unique)
- `epithet` (CharField, blank)
- `role` (choices: PIRATE, MARINE, REVOLUTIONARY, CIVILIAN, OTHER)
- `bounty` (IntegerField, default 0)
- `origin` (CharField, blank)
- `status` (choices: ALIVE, DEAD, UNKNOWN)
- `first_appearance_episode` (ForeignKey Episode)
- `description` (TextField, blank)
- `image_url` (URLField, blank)

### Relation 1-N: Arc → Episode
- **Arc:** name, saga, start_episode_number, end_episode_number, description
- **Episode:** number (unique), title, air_date, arc (FK)

### Relation N-N: Character ↔ Crew
- **Crew:** name (unique), ship_name, base_location, description, captain (FK Character)

### Autres entités
- **DevilFruit:** name, romanji, fruit_type, ability, weaknesses, rarity, status, first_appearance_arc, description
- **FruitHolder:** Table intermédiaire pour l'historique des détenteurs de fruits (devil_fruit, character, from_date, to_date, is_current)

## 🚀 Installation et démarrage

### Prérequis

- Docker et Docker Compose
- Python 3.11+ (pour développement local)
- Node.js 18+ et npm (pour le frontend)

### 1. Configuration initiale

```bash
# Cloner le projet
cd django-projet-op

# Copier le fichier d'environnement
cp .env.example .env

# Éditer .env si nécessaire (les valeurs par défaut fonctionnent)
```

### 2. Démarrage avec Docker

```bash
# Démarrer Oracle et Django
docker compose up -d

# Attendre que Oracle soit prêt (environ 1-2 minutes)
# Vérifier les logs: docker compose logs oracle

# Créer les migrations
docker compose exec web python manage.py makemigrations

# Appliquer les migrations
docker compose exec web python manage.py migrate

# Créer un superutilisateur
docker compose exec web python manage.py createsuperuser

# Générer des données de test
docker compose exec web python manage.py seed_onepiece \
  --reset \
  --characters 200 \
  --crews 30 \
  --fruits 80 \
  --arcs 20 \
  --episodes 200
```

### 3. Build du frontend React

```bash
# Installer les dépendances
cd frontend
npm install

# Build pour production
npm run build

# Le build sera dans frontend/dist/
# Il sera automatiquement servi par Django via collectstatic
```

### 4. Collecter les fichiers statiques

```bash
# Depuis le conteneur web
docker compose exec web python manage.py collectstatic --noinput
```

### 5. Accéder à l'application

- **Frontend:** http://localhost:8000
- **Admin Django:** http://localhost:8000/admin
- **API REST:** http://localhost:8000/api/
- **Stats Admin:** http://localhost:8000/admin/stats/

## 📡 API REST

L'API est en **lecture seule** (GET uniquement) avec pagination (10 éléments par page).

### Endpoints disponibles

- `GET /api/characters/` - Liste des personnages
- `GET /api/characters/{id}/` - Détail d'un personnage
- `GET /api/crews/` - Liste des équipages
- `GET /api/crews/{id}/` - Détail d'un équipage
- `GET /api/fruits/` - Liste des fruits du démon
- `GET /api/fruits/{id}/` - Détail d'un fruit
- `GET /api/arcs/` - Liste des arcs
- `GET /api/arcs/{id}/` - Détail d'un arc
- `GET /api/episodes/` - Liste des épisodes
- `GET /api/episodes/{id}/` - Détail d'un épisode

### Paramètres de recherche et tri

- **Recherche:** `?search=terme` (recherche dans les champs définis)
- **Tri:** `?ordering=champ` ou `?ordering=-champ` (ordre décroissant)
- **Pagination:** `?page=2`

### Exemples

```bash
# Rechercher des personnages
curl "http://localhost:8000/api/characters/?search=luffy"

# Trier par prime (décroissant)
curl "http://localhost:8000/api/characters/?ordering=-bounty"

# Page 2
curl "http://localhost:8000/api/characters/?page=2"
```

## 🎨 Frontend React

### Pages disponibles

- `/characters` - Liste des personnages avec recherche et pagination
- `/characters/:id` - Détail d'un personnage (équipages, fruits, rebonds)
- `/crews` - Liste des équipages
- `/crews/:id` - Détail d'un équipage (membres, rebonds)
- `/fruits` - Liste des fruits du démon avec recherche
- `/fruits/:id` - Détail d'un fruit (détenteurs, rebonds)
- `/arcs` - Liste des arcs avec recherche
- `/arcs/:id` - Détail d'un arc (épisodes)

### Navigation entre entités

Le frontend permet de naviguer entre les entités liées :
- Personnage → Équipages → Membres
- Personnage → Fruits du démon → Détenteurs
- Fruit → Arc de première apparition
- Équipage → Capitaine (personnage)

## 🔧 Admin Django

### Fonctionnalités

#### CRUD standard
- Interface d'administration complète pour tous les modèles
- Filtres, recherche, tri
- Inlines pour les relations (épisodes dans arcs, détenteurs dans fruits)

#### Export PDF
- Actions disponibles pour **Character** et **DevilFruit**
- Sélectionner un objet → Action "Exporter fiche PDF"
- Génère un PDF avec toutes les informations et relations

#### Export CSV
- Actions disponibles pour **Character** et **DevilFruit**
- Export en masse vers CSV

#### Statistiques avec graphiques
- Accès via `/admin/stats/` ou lien dans l'admin
- Graphique 1: Répartition des fruits par type (camembert)
- Graphique 2: Top 10 équipages par nombre de membres (barres horizontales)

#### Export JSON
- Commande management: `python manage.py export_json`
- Exporte toutes les données dans `/exports/opkb_export_TIMESTAMP.json`

## 🛠️ Commandes Management

### seed_onepiece

Génère des données aléatoires pour tester l'application.

```bash
python manage.py seed_onepiece [options]

Options:
  --reset              Vider toutes les tables avant de générer
  --characters N       Nombre de personnages (défaut: 50)
  --crews N            Nombre d'équipages (défaut: 10)
  --fruits N           Nombre de fruits (défaut: 30)
  --arcs N             Nombre d'arcs (défaut: 10)
  --episodes N         Nombre d'épisodes (défaut: 100)

Exemple:
  python manage.py seed_onepiece \
    --reset \
    --characters 200 \
    --crews 30 \
    --fruits 80 \
    --arcs 20 \
    --episodes 200
```

### export_json

Exporte toutes les données en JSON.

```bash
python manage.py export_json
```

Le fichier sera créé dans `/exports/opkb_export_TIMESTAMP.json`

## 🐳 Docker

### Services

- **oracle:** Base de données Oracle XE
  - Port: 1521
  - Volume: `oracle_data`
  - Healthcheck configuré

- **web:** Application Django
  - Port: 8000
  - Dépend de Oracle (attente du healthcheck)

### Commandes utiles

```bash
# Démarrer
docker compose up -d

# Voir les logs
docker compose logs -f web
docker compose logs -f oracle

# Arrêter
docker compose down

# Arrêter et supprimer les volumes
docker compose down -v

# Exécuter une commande dans le conteneur
docker compose exec web python manage.py <commande>
```

## 📝 Notes de développement

### Configuration Oracle

La connexion Oracle utilise les variables d'environnement :
- `DB_USER` (défaut: opkb_user)
- `DB_PASSWORD` (défaut: opkb_pass)
- `DB_SERVICE` (défaut: XE)
- `DB_HOST` (défaut: oracle)
- `DB_PORT` (défaut: 1521)

### Static files

Le frontend React est buildé dans `frontend/dist/` et servi par Django via `collectstatic`.

Le template `templates/index.html` sert l'application React en SPA (Single Page Application) avec un catch-all route.

### Contraintes logiques

- **FruitHolder:** Un seul détenteur actuel (`is_current=True`) par fruit du démon (validé dans `clean()` et `save()`)

## 🐛 Dépannage

### Oracle ne démarre pas

```bash
# Vérifier les logs
docker compose logs oracle

# Oracle peut prendre 1-2 minutes pour démarrer
# Vérifier le healthcheck
docker compose ps
```

### Erreur de connexion à Oracle

- Vérifier que Oracle est "healthy" dans `docker compose ps`
- Vérifier les variables d'environnement dans `.env`
- Vérifier que le service Oracle est accessible depuis le conteneur web

### Frontend ne s'affiche pas

- Vérifier que le build React a été fait: `cd frontend && npm run build`
- Vérifier que `collectstatic` a été exécuté
- Vérifier que les fichiers sont dans `staticfiles/`

### Erreurs de migration

```bash
# Supprimer et recréer les migrations
docker compose exec web python manage.py makemigrations
docker compose exec web python manage.py migrate
```

## 📚 Ressources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [React Documentation](https://react.dev/)
- [Vite Documentation](https://vitejs.dev/)
- [Oracle XE Docker](https://hub.docker.com/r/gvenzl/oracle-xe)

## 📄 Licence

Ce projet est un projet académique.

---

**Projet réalisé dans le cadre du B3 - [NOM] [PRENOM]**

