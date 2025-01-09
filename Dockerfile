# Этап 1: Сборка приложения
FROM node:18-alpine AS build

# Установка рабочей директории
WORKDIR /app

# Копирование package.json и package-lock.json
COPY package*.json ./

# Установка зависимостей
RUN npm install

# Копирование исходного кода
COPY . .

# Сборка приложения
RUN npm run build

# Этап 2: Настройка Nginx для обслуживания приложения
FROM nginx:stable-alpine

# Копирование собранных файлов из предыдущего этапа
COPY --from=build /app/build /usr/share/nginx/html

# Копирование кастомного конфигурационного файла Nginx (опционально)
# Если у вас есть файл конфигурации Nginx, например, nginx.conf, раскомментируйте следующую строку
# COPY nginx.conf /etc/nginx/nginx.conf

# Открытие порта 80
EXPOSE 80

# Запуск Nginx в форграунд режиме
CMD ["nginx", "-g", "daemon off;"]
