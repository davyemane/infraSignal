// 1. Classe pour gérer l'API
class API {
    async register(userData) {
        const response = await fetch('/api/register/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(userData)
        });
        return await response.json();
    }

    async login(credentials) {
        const response = await fetch('/api/login/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(credentials)
        });
        return await response.json();
    }
}

// 2. Classe pour gérer les WebSockets
class NotificationService {
    constructor() {
        this.socket = null;
        this.listeners = new Map();
    }

    connect() {
        this.socket = new WebSocket('ws://votreserveur/ws/notifications/');
        
        this.socket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            // Notifier tous les listeners pour ce type d'événement
            const listeners = this.listeners.get(data.type) || [];
            listeners.forEach(listener => listener(data));
        };
    }

    addListener(eventType, callback) {
        if (!this.listeners.has(eventType)) {
            this.listeners.set(eventType, []);
        }
        this.listeners.get(eventType).push(callback);
    }
}

// 3. Utilisation
const api = new API();
const notifications = new NotificationService();

// Connexion aux WebSockets
notifications.connect();

// Écoute des notifications d'inscription
notifications.addListener('user.registered', (data) => {
    console.log('Nouvel utilisateur:', data);
});

// Exemple d'inscription
async function registerUser() {
    try {
        const result = await api.register({
            phone_number: "0123456789",
            password: "motdepasse123"
        });
        console.log('Inscription réussie:', result);
    } catch (error) {
        console.error('Erreur d\'inscription:', error);
    }
}