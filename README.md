# API de Gestion des Utilisateurs avec WebSocket

Cette API permet de gérer l'authentification des utilisateurs et inclut des fonctionnalités de notifications en temps réel via WebSocket.

## 📋 Prérequis

- Python 3.8+
- Django 4.0+
- Django Channels
- Redis (pour les WebSockets)

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

### Inscription

**Endpoint**: `POST /api/register/`

**Payload**:
```json
{
    "phone_number": "0123456789",
    "password": "votreMotDePasse",
    "email": "user@example.com"
}
```

**Réponse**:
```json
{
    "refresh": "token_refresh...",
    "access": "token_access...",
    "user_id": 1,
    "phone_number": "0123456789"
}
```

### Connexion

**Endpoint**: `POST /api/login/`

**Payload**:
```json
{
    "phone_number": "0123456789",
    "password": "votreMotDePasse"
}
```

**Réponse**:
```json
{
    "refresh": "token_refresh...",
    "access": "token_access...",
    "user_id": 1,
    "phone_number": "0123456789"
}
```

## 🔌 WebSocket

### Connection WebSocket

URL de connexion: `ws://votre-domaine/ws/notifications/`

### Messages WebSocket

Les notifications sont envoyées dans le format suivant:

#### Notification d'inscription réussie
```json
{
    "type": "user.registered",
    "status": "success",
    "user_id": 1,
    "phone_number": "0123456789",
    "message": "Nouvel utilisateur inscrit"
}
```

#### Notification de connexion réussie
```json
{
    "type": "user.login",
    "status": "success",
    "user_id": 1,
    "phone_number": "0123456789",
    "message": "Utilisateur connecté"
}
```

## 💻 Exemple d'utilisation

### Avec JavaScript

```javascript
// Connexion WebSocket
const socket = new WebSocket('ws://localhost:8000/ws/notifications/');

socket.onopen = function(e) {
    console.log('Connexion WebSocket établie');
};

socket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    console.log('Message reçu:', data);
};

// Exemple d'appel API avec fetch
async function register(userData) {
    try {
        const response = await fetch('http://localhost:8000/api/register/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(userData)
        });
        const data = await response.json();
        console.log('Inscription réussie:', data);
    } catch (error) {
        console.error('Erreur:', error);
    }
}
```

### Avec Python

```python
import websockets
import asyncio
import json
import requests

# Appel API REST
def register_user(phone_number, password):
    response = requests.post(
        'http://localhost:8000/api/register/',
        json={
            'phone_number': phone_number,
            'password': password
        }
    )
    return response.json()

# Connection WebSocket
async def connect_websocket():
    uri = "ws://localhost:8000/ws/notifications/"
    async with websockets.connect(uri) as websocket:
        while True:
            message = await websocket.recv()
            print(f"< {message}")

# Utilisation
if __name__ == "__main__":
    # Exemple d'inscription
    result = register_user("0123456789", "password123")
    print(result)
    
    # Écoute des notifications
    asyncio.get_event_loop().run_until_complete(connect_websocket())
```

## 🛠️ Environnement de développement

Variables d'environnement nécessaires dans `.env`:

```env
DEBUG=True
SECRET_KEY=votre_clef_secrete
ALLOWED_HOSTS=localhost,127.0.0.1
REDIS_URL=redis://localhost:6379
```

## 📝 Tests

Pour exécuter les tests :
```bash
python manage.py test
```

## 🔒 Sécurité

- Les mots de passe sont hashés avec Argon2
- Utilisation de JWT pour l'authentification
- Protection CSRF activée
- Validation des données entrantes

## 🤝 Contribution

1. Forkez le projet
2. Créez votre branche (`git checkout -b feature/AmazingFeature`)
3. Committez vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Poussez vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

## 📄 License

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.