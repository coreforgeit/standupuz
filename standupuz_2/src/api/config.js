// src/api/config.js

// 1) Сначала пробуем взять из .env, иначе — дефолт localhost:
// export const API_BASE_URL = window.location.origin;
export const API_BASE_URL = 'http://localhost:8000';

// 2) Перечисляем все пути вашего API
export const API_PATHS = {
  events: '/api/event/',
  info:   '/api/info/',
};
