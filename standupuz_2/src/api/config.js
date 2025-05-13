// src/api/config.js

// 1) Сначала пробуем взять из .env, иначе — дефолт localhost:
export const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://standupcomedy.uz/';

// 2) Перечисляем все пути вашего API
export const API_PATHS = {
  events: '/api/event/',
  info:   '/api/info/',
};
