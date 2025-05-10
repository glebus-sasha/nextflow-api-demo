# frontend/Dockerfile

FROM node:16-slim

# Устанавливаем рабочую директорию
WORKDIR /frontend

# Копируем package.json и устанавливаем зависимости
COPY frontend/package.json frontend/package-lock.json ./
RUN npm install

COPY frontend/public /frontend/public
COPY frontend/src /frontend/src

# Собираем проект
RUN npm run build

EXPOSE 3000
CMD ["npm", "start"]