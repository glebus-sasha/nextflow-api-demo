import React from 'react';
import ReactDOM from 'react-dom/client';  // изменили импорт

import App from './App';

// Получаем корневой элемент
const root = ReactDOM.createRoot(document.getElementById('root'));

// Используем createRoot для рендеринга приложения
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
