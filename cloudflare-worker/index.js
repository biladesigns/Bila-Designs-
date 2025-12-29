/**
 * Bila Designs - Brief IA API Worker
 * Cloudflare Worker pour proxy sécurisé vers OpenAI
 *
 * Variables d'environnement requises:
 * - OPENAI_API_KEY: Clé API OpenAI
 */

// Configuration
const ALLOWED_ORIGINS = [
  'https://biladesigns.com',
  'https://www.biladesigns.com',
  'http://localhost:8000', // Dev local
  'http://127.0.0.1:8000'
];

const RATE_LIMIT = 10; // Requêtes par minute par IP
const RATE_LIMIT_WINDOW = 60 * 1000; // 1 minute en ms

// Store simple pour rate limiting (reset à chaque redéploiement)
const rateLimitStore = new Map();

// Prompts système optimisés
const PROMPTS = {
  // NOUVEAU: Suggestions intelligentes par secteur
  sector_suggestions: (context) => `Tu es un expert en stratégie digitale et en création de sites web. Tu as analysé des centaines de sites web performants dans chaque secteur.

SECTEUR: ${context.sector}
${context.target ? `CIBLE: ${context.target}` : ''}

Analyse les MEILLEURS sites web de ${context.sector} (les plus performants, les mieux référencés, ceux qui convertissent le mieux) et donne-moi:

1. Les 5-7 PAGES que tous les meilleurs sites de ce secteur ont en commun
2. Les 8-10 MOTS-CLÉS les plus recherchés par les clients de ce secteur sur Google
3. Les 3-4 FONCTIONNALITÉS indispensables pour ce type de site

Pense comme un client qui cherche un ${context.sector}. Quels mots tape-t-il sur Google ? Quelles pages s'attend-il à trouver ?

IMPORTANT: Sois SPÉCIFIQUE au secteur. Pas de réponses génériques.

Réponds UNIQUEMENT en JSON valide:
{
  "pages": ["Page 1", "Page 2", ...],
  "keywords": ["mot-clé 1", "mot-clé 2", ...],
  "features": ["fonctionnalité 1", "fonctionnalité 2", ...],
  "tip": "Un conseil spécifique et actionnable pour ce secteur (1 phrase)"
}`,

  pages: (context) => `Tu es un expert en création de sites web.
Secteur: ${context.sector}
Cible: ${context.target}
Description: ${context.description || 'Non spécifiée'}

Suggère 3 à 5 pages web essentielles pour ce type d'entreprise.
Réponds uniquement avec une liste JSON: ["page1", "page2", ...]`,

  content: (context) => `Tu es un rédacteur web expert spécialisé en UX writing.
Page: ${context.page}
Entreprise: ${context.business}
Secteur: ${context.sector}
Cible: ${context.target}
Description entreprise: ${context.description || 'Non spécifiée'}
${context.userNotes ? `Notes du client pour cette page:\n${context.userNotes}` : ''}

Écris le contenu de cette page web de manière STRUCTURÉE comme une vraie page.
${context.userNotes ? 'Base-toi sur les notes du client.' : ''}

Format attendu:
# [Titre principal accrocheur]

## [Section 1]
[Texte de la section - 2-3 phrases]

## [Section 2]
[Texte de la section - 2-3 phrases]

## [Section 3 si pertinent]
[Texte de la section - 2-3 phrases]

Règles:
- Maximum 150 mots au total
- Utilise # pour le titre principal et ## pour les sous-titres
- Adapte les sections au type de page (ex: Accueil = accroche + valeurs, Services = liste services, Contact = invitation)
- Ton professionnel mais accessible`,

  seo: (context) => `Tu es un expert SEO.
Mots-clés: ${context.keywords.join(', ')}
Secteur: ${context.sector}
Page: ${context.page || 'Page d\'accueil'}
${context.pageNotes ? `Contenu prévu pour cette page:\n${context.pageNotes}` : ''}

Propose une structure SEO optimisée pour cette page spécifique.
Format de réponse (JSON uniquement):
{
  "h1": "Titre principal optimisé pour SEO",
  "h2": ["Sous-titre 1", "Sous-titre 2", "Sous-titre 3"],
  "metaDescription": "Description meta (max 160 caractères)"
}`,

  // Suggestions de mots-clés basées sur la description des services
  keyword_suggestions: (context) => `Tu es un expert SEO et marketing digital.

ENTREPRISE: ${context.business || 'Non spécifiée'}
SECTEUR: ${context.sector || 'Non spécifié'}
DESCRIPTION DES SERVICES:
${context.description}

Analyse cette description et génère les 8-10 MOTS-CLÉS les plus pertinents que les clients potentiels rechercheraient sur Google pour trouver ces services.

Pense comme un client qui cherche ces services. Quels termes utiliserait-il ?

Inclus:
- Des mots-clés principaux (1-2 mots)
- Des mots-clés longue traîne (3-4 mots)
- Des mots-clés locaux si pertinent

Réponds UNIQUEMENT en JSON valide:
{
  "keywords": ["mot-clé 1", "mot-clé 2", ...]
}`
};

// Headers CORS
function corsHeaders(origin) {
  const allowedOrigin = ALLOWED_ORIGINS.includes(origin) ? origin : ALLOWED_ORIGINS[0];
  return {
    'Access-Control-Allow-Origin': allowedOrigin,
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '86400',
  };
}

// Rate limiting simple
function checkRateLimit(ip) {
  const now = Date.now();
  const record = rateLimitStore.get(ip);

  if (!record || now - record.timestamp > RATE_LIMIT_WINDOW) {
    rateLimitStore.set(ip, { count: 1, timestamp: now });
    return true;
  }

  if (record.count >= RATE_LIMIT) {
    return false;
  }

  record.count++;
  return true;
}

// Validation des données d'entrée
function validateRequest(data) {
  const validTypes = ['pages', 'content', 'seo', 'sector_suggestions', 'keyword_suggestions'];

  if (!data.type || !validTypes.includes(data.type)) {
    return { valid: false, error: 'Type invalide' };
  }

  if (!data.context || typeof data.context !== 'object') {
    return { valid: false, error: 'Context requis' };
  }

  // Validation spécifique par type
  switch (data.type) {
    case 'sector_suggestions':
      if (!data.context.sector) {
        return { valid: false, error: 'sector requis' };
      }
      break;
    case 'pages':
      if (!data.context.sector || !data.context.target) {
        return { valid: false, error: 'sector et target requis pour les suggestions de pages' };
      }
      break;
    case 'content':
      if (!data.context.page || !data.context.business || !data.context.sector) {
        return { valid: false, error: 'page, business et sector requis pour le contenu' };
      }
      break;
    case 'seo':
      if (!data.context.keywords || !Array.isArray(data.context.keywords) || data.context.keywords.length === 0) {
        return { valid: false, error: 'keywords (array) requis pour SEO' };
      }
      break;
    case 'keyword_suggestions':
      if (!data.context.description) {
        return { valid: false, error: 'description requise pour keyword_suggestions' };
      }
      break;
  }

  return { valid: true };
}

// Appel à l'API OpenAI
async function callOpenAI(prompt, env) {
  const response = await fetch('https://api.openai.com/v1/chat/completions', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${env.OPENAI_API_KEY}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      model: 'gpt-4o-mini',
      messages: [
        { role: 'user', content: prompt }
      ],
      max_tokens: 500,
      temperature: 0.7,
    }),
  });

  if (!response.ok) {
    const error = await response.text();
    throw new Error(`OpenAI API error: ${response.status} - ${error}`);
  }

  const result = await response.json();
  return result.choices[0].message.content;
}

// Parse la réponse selon le type
function parseResponse(type, rawResponse) {
  try {
    switch (type) {
      case 'sector_suggestions':
        // Extraire le JSON complet
        const sectorMatch = rawResponse.match(/\{[\s\S]*\}/);
        if (sectorMatch) {
          const parsed = JSON.parse(sectorMatch[0]);
          return {
            pages: parsed.pages || [],
            keywords: parsed.keywords || [],
            features: parsed.features || [],
            tip: parsed.tip || ''
          };
        }
        return { pages: [], keywords: [], features: [], tip: '' };

      case 'pages':
        // Extraire le JSON de la réponse
        const pagesMatch = rawResponse.match(/\[.*\]/s);
        if (pagesMatch) {
          return { suggestions: JSON.parse(pagesMatch[0]) };
        }
        // Fallback: split par lignes
        return { suggestions: rawResponse.split('\n').filter(l => l.trim()).slice(0, 5) };

      case 'content':
        return { content: rawResponse.trim() };

      case 'seo':
        // Extraire le JSON de la réponse
        const seoMatch = rawResponse.match(/\{[\s\S]*\}/);
        if (seoMatch) {
          return JSON.parse(seoMatch[0]);
        }
        return { h1: rawResponse, h2: [], metaDescription: '' };

      case 'keyword_suggestions':
        // Extraire le JSON avec les keywords
        const keywordMatch = rawResponse.match(/\{[\s\S]*\}/);
        if (keywordMatch) {
          const parsed = JSON.parse(keywordMatch[0]);
          return { keywords: parsed.keywords || [] };
        }
        return { keywords: [] };

      default:
        return { raw: rawResponse };
    }
  } catch (e) {
    return { raw: rawResponse };
  }
}

// Handler principal
export default {
  async fetch(request, env, ctx) {
    const origin = request.headers.get('Origin') || '';
    const headers = corsHeaders(origin);

    // Gestion CORS preflight
    if (request.method === 'OPTIONS') {
      return new Response(null, { status: 204, headers });
    }

    // Vérifier la méthode
    if (request.method !== 'POST') {
      return new Response(JSON.stringify({
        success: false,
        error: 'Méthode non autorisée'
      }), {
        status: 405,
        headers: { ...headers, 'Content-Type': 'application/json' },
      });
    }

    // Rate limiting
    const clientIP = request.headers.get('CF-Connecting-IP') || 'unknown';
    if (!checkRateLimit(clientIP)) {
      return new Response(JSON.stringify({
        success: false,
        error: 'Trop de requêtes. Réessayez dans une minute.'
      }), {
        status: 429,
        headers: { ...headers, 'Content-Type': 'application/json' },
      });
    }

    try {
      // Parser le body
      const data = await request.json();

      // Valider la requête
      const validation = validateRequest(data);
      if (!validation.valid) {
        return new Response(JSON.stringify({
          success: false,
          error: validation.error
        }), {
          status: 400,
          headers: { ...headers, 'Content-Type': 'application/json' },
        });
      }

      // Générer le prompt
      const prompt = PROMPTS[data.type](data.context);

      // Appeler OpenAI
      const rawResponse = await callOpenAI(prompt, env);

      // Parser la réponse
      const parsedData = parseResponse(data.type, rawResponse);

      return new Response(JSON.stringify({
        success: true,
        data: parsedData
      }), {
        status: 200,
        headers: { ...headers, 'Content-Type': 'application/json' },
      });

    } catch (error) {
      console.error('Error:', error);
      return new Response(JSON.stringify({
        success: false,
        error: 'Erreur serveur. Réessayez plus tard.'
      }), {
        status: 500,
        headers: { ...headers, 'Content-Type': 'application/json' },
      });
    }
  },
};
