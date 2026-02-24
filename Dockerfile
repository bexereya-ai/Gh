FROM node:18-slim

# Устанавливаем Python (на всякий случай)
RUN apt-get update && apt-get install -y python3 python3-pip

# Создаем рабочую директорию
WORKDIR /app

# Копируем файлы
COPY package*.json ./
COPY main.py ./
COPY bot.js ./

# Устанавливаем зависимости Node.js
RUN npm install

# Устанавливаем Python зависимости (если есть)
RUN pip3 install -r requirements.txt || true

# Команда запуска
CMD ["node", "bot.js"]
