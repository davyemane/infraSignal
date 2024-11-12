# API de Gestion des Utilisateurs et Points Sensibles avec WebSocket

Cette API permet de gérer l'authentification des utilisateurs, les points sensibles sur la carte et inclut des fonctionnalités de notifications en temps réel via WebSocket.

## 📋 Prérequis

- Python 3.8+
- Django 4.0+
- Django Channels
- Redis (pour les WebSockets)
- PostGIS (pour les fonctionnalités géospatiales)

## 🚀 Installation

1. Clonez le dépôt
```bash
git clone [votre-repo]
cd [infraSignal]
```

2. Créez un environnement virtuel
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
.\venv\Scripts\activate  # Windows
```

3. Installez les dépendances
```bash
pip install -r requirements.txt
```

4. Configurez la base de données
```bash
python manage.py migrate
```

5. Lancez le serveur
```bash
python manage.py runserver
```

## 🔑 Authentification API

[Section authentification existante reste identique...]

## 📍 API Points Sensibles

### Types de Problèmes

#### Lister les types de problèmes
**Endpoint**: `GET /api/problem-types/`

**Réponse**:
```json
[
    {
        "id": 1,
        "name": "Nid de poule",
        "description": "Trou dans la chaussée",
        "icon": "pothole-icon"
    }
]
```

### Points Sensibles

#### Créer un point sensible
**Endpoint**: `POST /api/sensitive-points/`

**Payload**:
```json
{
    "problem_type": 1,
    "latitude": 48.8566,
    "longitude": 2.3522,
    "sector": "Centre-ville",
    "description": "Large nid de poule dangereux"
}
```

**Réponse**:
```json
{
    "id": 1,
    "created_by": "0123456789",
    "problem_type": {
        "id": 1,
        "name": "Nid de poule",
        "description": "Trou dans la chaussée",
        "icon": "pothole-icon"
    },
    "latitude": 48.8566,
    "longitude": 2.3522,
    "sector": "Centre-ville",
    "description": "Large nid de poule dangereux",
    "status": "PENDING",
    "created_at": "2024-11-12T10:30:00Z",
    "updated_at": "2024-11-12T10:30:00Z",
    "images": []
}
```

#### Ajouter une image à un point
**Endpoint**: `POST /api/sensitive-points/{id}/add_image/`

**Payload**: `multipart/form-data`
```
image: [fichier image]
description: "Vue du nid de poule"
```

#### Filtrer les points sensibles
**Endpoint**: `GET /api/sensitive-points/?problem_type=1&lat=48.8566&lng=2.3522&radius=1000`

Paramètres de filtrage:
- `problem_type`: ID du type de problème
- `lat`: Latitude du centre de recherche
- `lng`: Longitude du centre de recherche
- `radius`: Rayon de recherche en mètres

#### Mettre à jour le statut
**Endpoint**: `POST /api/sensitive-points/{id}/update_status/`

**Payload**:
```json
{
    "status": "IN_PROGRESS"
}
```

## 🔌 WebSocket

[Section WebSocket existante...]

### Nouvelles Notifications WebSocket pour les Points Sensibles

#### Notification de nouveau point sensible
```json
{
    "type": "sensitive_point.created",
    "message": "Nouveau point sensible signalé dans Centre-ville",
    "point_id": 1,
    "sector": "Centre-ville"
}
```

## 💻 Exemple d'utilisation

### Avec JavaScript

```javascript
// Exemple précédent...

// Création d'un point sensible
async function createSensitivePoint(pointData) {
    try {
        const response = await fetch('http://localhost:8000/api/sensitive-points/', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(pointData)
        });
        const data = await response.json();
        console.log('Point sensible créé:', data);
    } catch (error) {
        console.error('Erreur:', error);
    }
}

// Ajout d'une image
async function addImage(pointId, imageFile) {
    const formData = new FormData();
    formData.append('image', imageFile);
    
    try {
        const response = await fetch(`http://localhost:8000/api/sensitive-points/${pointId}/add_image/`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
            },
            body: formData
        });
        const data = await response.json();
        console.log('Image ajoutée:', data);
    } catch (error) {
        console.error('Erreur:', error);
    }
}
```

## 🛠️ Environnement de développement

Variables d'environnement nécessaires dans `.env`:

```env
DEBUG=True
SECRET_KEY=votre_clef_secrete
ALLOWED_HOSTS=localhost,127.0.0.1
REDIS_URL=redis://localhost:6379
POSTGIS_DATABASE=nom_de_votre_base
```

## 📝 Tests

[Section tests existante reste identique...]

## 🔒 Sécurité

[Section sécurité existante...]
- Validation géospatiale des coordonnées

## 🤝 Contribution

[Section contribution existante reste identique...]

## 📄 License

[Section licence existante reste identique...]