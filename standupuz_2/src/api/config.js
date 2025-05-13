// src/api/config.js
const ORIGIN = window.location.origin;

// 1) Сначала пробуем взять из .env, иначе — дефолт localhost:
export const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || ORIGIN;

// 2) Перечисляем все пути вашего API
export const API_PATHS = {
  events: '/api/event/',
  info:   '/api/info/',
};
