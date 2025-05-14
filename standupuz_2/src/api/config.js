// src/api/config.js

const API_BASE_URL =
  process.env.NODE_ENV === 'development'
    ? 'http://localhost'
    : window.location.origin;

// экспортируем уже готовую константу
export { API_BASE_URL };

// 2) Перечисляем все пути вашего API
export const API_PATHS = {
  events: '/api/event/',
  info: '/api/info/',
};
