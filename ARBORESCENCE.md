# Arborescence du projet One Piece Knowledge Base

```
django-projet-op/
│
├── opkb/                          # Configuration principale Django
│   ├── __init__.py
│   ├── settings.py               # Configuration (Oracle, DRF, static files)
│   ├── urls.py                   # URLs principales + catch-all pour SPA
│   ├── wsgi.py
│   └── asgi.py
│
├── knowledge/                     # Application Django principale
│   ├── __init__.py
│   ├── apps.py
│   ├── models.py                 # Modèles: Character, Crew, Arc, Episode, DevilFruit, FruitHolder
│   ├── admin.py                  # Admin avec exports PDF/CSV, graphiques matplotlib
│   ├── serializers.py            # Serializers DRF (listes + détails)
│   ├── views.py                  # ViewSets DRF + vue stats admin
│   ├── urls.py                   # Routes API REST
│   │
│   └── management/
│       └── commands/
│           ├── __init__.py
│           ├── seed_onepiece.py  # Génération de données aléatoires
│           └── export_json.py    # Export JSON de la base
│
├── frontend/                      # Application React + Vite
│   ├── package.json
│   ├── vite.config.js
│   ├── index.html
│   │
│   └── src/
│       ├── main.jsx              # Point d'entrée React
│       ├── App.jsx               # Composant principal + Router
│       ├── App.css
│       ├── index.css
│       │
│       └── pages/                # Pages React
│           ├── CharactersList.jsx
│           ├── CharacterDetail.jsx
│           ├── CrewsList.jsx
│           ├── CrewDetail.jsx
│           ├── FruitsList.jsx
│           ├── FruitDetail.jsx
│           ├── ArcsList.jsx
│           └── ArcDetail.jsx
│
├── templates/                     # Templates Django
│   ├── index.html                # Template SPA React (catch-all)
│   └── admin/
│       └── stats.html            # Page stats avec graphiques matplotlib
│
├── static/                       # Fichiers statiques (collectstatic)
├── staticfiles/                  # Fichiers statiques collectés (généré)
├── media/                        # Fichiers média (stats, uploads)
├── exports/                      # Exports JSON (généré)
│
├── docker-compose.yml            # Configuration Docker (Oracle + Django)
├── Dockerfile                    # Image Docker pour Django
├── requirements.txt              # Dépendances Python
├── .env.example                  # Exemple de variables d'environnement
├── .gitignore
├── manage.py                     # Script de gestion Django
│
├── README.md                     # Documentation principale
└── ARBORESCENCE.md              # Ce fichier
```

## Fichiers clés

### Backend Django

- **opkb/settings.py**: Configuration Oracle, DRF, static files, CORS
- **knowledge/models.py**: 6 modèles avec relations 1-N (Arc→Episode) et N-N (Character↔Crew)
- **knowledge/admin.py**: Admin avec actions PDF/CSV, inlines, vue stats
- **knowledge/serializers.py**: Serializers pour listes et détails avec relations
- **knowledge/views.py**: ViewSets ReadOnlyModelViewSet avec search/ordering
- **knowledge/urls.py**: Routes API REST

### Frontend React

- **frontend/src/App.jsx**: Router React avec toutes les routes
- **frontend/src/pages/**: 8 pages (4 listes + 4 détails)
- **frontend/vite.config.js**: Configuration Vite pour build vers `/static/`

### Docker

- **docker-compose.yml**: Services Oracle et Django
- **Dockerfile**: Image avec Oracle Instant Client

### Commandes Management

- **seed_onepiece.py**: Génération de données avec Faker
- **export_json.py**: Export complet en JSON

