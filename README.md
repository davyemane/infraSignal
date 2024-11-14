# 🛣️ InfraSignal API

Une API complète pour la gestion des utilisateurs et des points sensibles d'infrastructure avec support WebSocket pour les notifications en temps réel.

## 📋 Table des matières

- [Prérequis](#prérequis)
- [Installation](#installation)
- [Configuration](#configuration)
- [Documentation API](#documentation-api)
  - [Authentification](#authentification)
  - [Points Sensibles](#points-sensibles)
  - [WebSocket](#websocket)
- [Exemples d'utilisation](#exemples-dutilisation)
- [Tests](#tests)
- [Contribution](#contribution)
- [Sécurité](#sécurité)
- [License](#license)

## Prérequis

- Python 3.8+
- Django 4.0+
- Django Channels
- Redis (pour les WebSockets)
- PostGIS (pour les fonctionnalités géospatiales)

## Installation

1. **Clonez le dépôt**
```bash
git clone https://github.com/davyemane/infraSignal.git
cd infraSignal
```

2. **Créez l'environnement virtuel**
```bash
python -m venv venv

# Linux/Mac
source venv/bin/activate

# Windows
.\venv\Scripts\activate
```

3. **Installez les dépendances**
```bash
pip install -r requirements.txt
```

4. **Configurez la base de données**
```bash
python manage.py migrate
```

5. **Lancez le serveur**
```bash
python manage.py runserver
```

## Configuration

### Variables d'environnement

Créez un fichier `.env` à la racine du projet :

```env
DEBUG=True
SECRET_KEY=votre_clef_secrete
ALLOWED_HOSTS=localhost,127.0.0.1
REDIS_URL=redis://localhost:6379
POSTGIS_DATABASE=nom_de_votre_base
```

## Documentation API

### Authentification

#### Inscription
`POST /api/register/`
```json
{
    "phone_number": "0123456789",
    "password": "votreMotDePasse",
    "email": "user@example.com"
}
```

#### Connexion
`POST /api/login/`
```json
{
    "phone_number": "0123456789",
    "password": "votreMotDePasse"
}
```

### Points Sensibles

#### Liste des types de problèmes
`GET /api/problem-types/`

#### Création d'un point sensible
`POST /api/sensitive-points/`
```json
{
    "problem_type": 1,
    "latitude": 48.8566,
    "longitude": 2.3522,
    "sector": "Centre-ville",
    "description": "Large nid de poule dangereux"
}
```

#### Ajout d'image
`POST /api/sensitive-points/{id}/add_image/`
```
Content-Type: multipart/form-data
image: [fichier image]
description: "Vue du nid de poule"
```

### WebSocket

#### Connection
```javascript
const socket = new WebSocket('ws://votre-domaine/ws/notifications/');
```

#### Format des notifications
```json
{
    "type": "sensitive_point.created",
    "message": "Nouveau point sensible signalé",
    "point_id": 1,
    "sector": "Centre-ville"
}
```

## Exemples d'utilisation

### JavaScript/React
```javascript
// Connection WebSocket
const socket = new WebSocket('ws://localhost:8000/ws/notifications/');

// Création d'un point sensible
async function createSensitivePoint(pointData, token) {
    const response = await fetch('http://localhost:8000/api/sensitive-points/', {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(pointData)
    });
    return response.json();
}
```

## Tests

```bash
# Exécuter tous les tests
python manage.py test

# Exécuter les tests d'une application spécifique
python manage.py test app_name
```

## Sécurité

- Hachage des mots de passe avec Argon2
- Authentification JWT
- Protection CSRF
- Validation des données et coordonnées géospatiales
- Validation géospatiale des coordonnées

## Contribution

1. Forkez le projet
2. Créez votre branche (`git checkout -b feature/AmazingFeature`)
3. Committez vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Poussez vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

## License

<!-- Ce projet est sous licence UIECC. Voir le fichier [`LICENSE`](LICENSE) pour plus de détails. -->

---

Développé avec ❤️ par [davyemane](https://github.com/davyemane)