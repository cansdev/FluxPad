// API Configuration
export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

// Production API URL for Railway
const PRODUCTION_API_URL = 'https://fluxpad-api-production.up.railway.app'

// Use production URL if we're in production environment
export const RESOLVED_API_BASE_URL = process.env.NODE_ENV === 'production' && !process.env.NEXT_PUBLIC_API_URL 
  ? PRODUCTION_API_URL 
  : API_BASE_URL

// API endpoints
export const API_ENDPOINTS = {
  LOGIN: `${RESOLVED_API_BASE_URL}/auth/login`,
  REGISTER: `${RESOLVED_API_BASE_URL}/auth/register`,
  ME: `${RESOLVED_API_BASE_URL}/auth/me`,
  REFRESH: `${RESOLVED_API_BASE_URL}/auth/refresh`,
  PING: `${RESOLVED_API_BASE_URL}/ping`,
} as const