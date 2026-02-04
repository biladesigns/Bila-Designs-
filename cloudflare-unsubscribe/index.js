/**
 * Bila Designs - Unsubscribe Worker
 * Gère les désabonnements email avec stockage KV
 */

const CORS_HEADERS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type',
};

// Clé API simple pour sécuriser l'endpoint /list (à changer en production)
const API_KEY = 'bila-unsubscribe-key-2025';

export default {
  async fetch(request, env, ctx) {
    // Handle CORS preflight
    if (request.method === 'OPTIONS') {
      return new Response(null, { headers: CORS_HEADERS });
    }

    const url = new URL(request.url);
    const path = url.pathname;

    try {
      // POST /unsubscribe - Ajouter un email à la liste de désabonnement
      if (path === '/unsubscribe' && request.method === 'POST') {
        const body = await request.json();
        const email = body.email?.trim().toLowerCase();

        if (!email || !isValidEmail(email)) {
          return jsonResponse({ error: 'Email invalide' }, 400);
        }

        // Stocker l'email avec timestamp
        await env.UNSUBSCRIBE_KV.put(email, JSON.stringify({
          unsubscribed_at: new Date().toISOString(),
          ip: request.headers.get('CF-Connecting-IP') || 'unknown'
        }));

        return jsonResponse({ success: true, message: 'Désabonnement confirmé' }, 200);
      }

      // GET /check?email=xxx - Vérifier si un email est désabonné
      if (path === '/check' && request.method === 'GET') {
        const email = url.searchParams.get('email')?.trim().toLowerCase();

        if (!email) {
          return jsonResponse({ error: 'Email requis' }, 400);
        }

        const data = await env.UNSUBSCRIBE_KV.get(email);
        const isUnsubscribed = data !== null;

        return jsonResponse({ email, unsubscribed: isUnsubscribed }, 200);
      }

      // GET /list - Récupérer la liste complète des désabonnés (protégé par API key)
      if (path === '/list' && request.method === 'GET') {
        const apiKey = url.searchParams.get('key') || request.headers.get('X-API-Key');

        if (apiKey !== API_KEY) {
          return jsonResponse({ error: 'Non autorisé' }, 401);
        }

        const list = await env.UNSUBSCRIBE_KV.list();
        const emails = list.keys.map(key => key.name);

        return jsonResponse({ count: emails.length, emails }, 200);
      }

      // GET /stats - Statistiques publiques
      if (path === '/stats' && request.method === 'GET') {
        const list = await env.UNSUBSCRIBE_KV.list();
        return jsonResponse({ total_unsubscribed: list.keys.length }, 200);
      }

      // 404 for unknown routes
      return jsonResponse({ error: 'Route non trouvée' }, 404);

    } catch (error) {
      console.error('Error:', error);
      return jsonResponse({ error: 'Erreur serveur' }, 500);
    }
  }
};

function isValidEmail(email) {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}

function jsonResponse(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: {
      'Content-Type': 'application/json',
      ...CORS_HEADERS
    }
  });
}
