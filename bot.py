import asyncio
from mcstatus import JavaServer
import subprocess
import time
import logging
import os
import signal
import sys

# Настройки
SERVER_IP = "RexWorld.aternos.me"
SERVER_PORT = 28068
BOT_USERNAME = "IrnaMoret345"
BOT_PASSWORD = "uiop0035"

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class MinecraftBot:
    def __init__(self):
        self.process = None
        self.running = True
        
    def connect(self):
        """Подключение к серверу через mclib (Python) или mineflayer (Node.js)"""
        try:
            # Способ 1: Через Node.js (более стабильно)
            self.start_node_bot()
            
            # Способ 2: Через Python (если нет Node.js)
            # self.start_python_bot()
            
        except Exception as e:
            logger.error(f"Ошибка подключения: {e}")
            time.sleep(10)
            self.reconnect()
    
    def start_node_bot(self):
        """Запуск Node.js бота (рекомендуется)"""
        node_code = f"""
        const mineflayer = require('mineflayer');
        
        const bot = mineflayer.createBot({{
            host: '{SERVER_IP}',
            port: {SERVER_PORT},
            username: '{BOT_USERNAME}',
            version: '1.16.5'  // Укажи версию сервера
        }});
        
        bot.on('login', () => {{
            console.log('Бот зашел на сервер');
            
            // Отправляем команды регистрации и входа
            setTimeout(() => {{
                bot.chat('/register {BOT_PASSWORD}');
                console.log('Отправлена команда /register');
            }}, 3000);
            
            setTimeout(() => {{
                bot.chat('/login {BOT_PASSWORD}');
                console.log('Отправлена команда /login');
            }}, 4000);
        }});
        
        // Прыгаем каждые 3 минуты
        setInterval(() => {{
            bot.setControlState('jump', true);
            setTimeout(() => bot.setControlState('jump', false), 500);
            console.log('Бот прыгнул');
        }}, 180000);
        
        // Проверка соединения
        setInterval(() => {{
            if (!bot.entity) {{
                console.log('Потеряно соединение, перезапуск...');
                process.exit(1);
            }}
        }}, 30000);
        
        bot.on('end', (reason) => {{
            console.log('Бот отключен:', reason);
            process.exit(1);
        }});
        
        bot.on('error', (err) => {{
            console.log('Ошибка:', err);
        }});
        
        console.log('Запуск бота {BOT_USERNAME}...');
        """
        
        # Сохраняем Node.js код во временный файл
        with open('bot.js', 'w') as f:
            f.write(node_code)
        
        # Запускаем Node.js процесс
        self.process = subprocess.Popen(
            ['node', 'bot.js'],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )
        
        logger.info(f"Node.js бот запущен с PID: {self.process.pid}")
    
    def start_python_bot(self):
        """Запуск Python бота (альтернатива)"""
        python_code = f"""
import asyncio
import time
from quarry.net.client import ClientFactory, SpawningClient

class BotClient(SpawningClient):
    def packet_login_success(self, buff):
        super().packet_login_success(buff)
        print("Бот зашел на сервер")
        
        # Отправляем команды
        asyncio.get_event_loop().call_later(3, lambda: self.send_chat('/register {BOT_PASSWORD}'))
        asyncio.get_event_loop().call_later(4, lambda: self.send_chat('/login {BOT_PASSWORD}'))
        
        # Запускаем прыжки
        self.jump_task = asyncio.get_event_loop().call_later(180, self.jump_loop)
    
    def jump_loop(self):
        """Прыжки каждые 3 минуты"""
        self.send_chat('/jump')
        print("Бот прыгнул")
        self.jump_task = asyncio.get_event_loop().call_later(180, self.jump_loop)
    
    def send_chat(self, message):
        """Отправка сообщения в чат"""
        self.send_packet(
            "chat_message",
            self.buff_type.pack_string(message)
        )
        print(f"Отправлено: {{message}}")

class BotFactory(ClientFactory):
    protocol = BotClient

def main():
    factory = BotFactory()
    factory.connect(
        host='{SERVER_IP}',
        port={SERVER_PORT}
    )
    print(f"Подключение к {{SERVER_IP}}:{{SERVER_PORT}}...")
    
    try:
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
"""
        
        # Сохраняем Python код
        with open('python_bot.py', 'w') as f:
            f.write(python_code)
        
        # Запускаем Python процесс
        self.process = subprocess.Popen(
            ['python3', 'python_bot.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )
        
        logger.info(f"Python бот запущен с PID: {self.process.pid}")
    
    def monitor(self):
        """Мониторинг процесса бота"""
        while self.running:
            if self.process:
                # Проверяем, жив ли процесс
                poll = self.process.poll()
                if poll is not None:
                    logger.warning(f"Бот остановлен с кодом: {poll}")
                    logger.info("Перезапуск через 10 секунд...")
                    time.sleep(10)
                    self.connect()
            
            time.sleep(5)
    
    def reconnect(self):
        """Переподключение при отключении"""
        logger.info("Попытка переподключения...")
        if self.process:
            self.process.kill()
        self.connect()
    
    def stop(self):
        """Остановка бота"""
        self.running = False
        if self.process:
            self.process.terminate()
            logger.info("Бот остановлен")

def install_dependencies():
    """Установка зависимостей"""
    try:
        # Для Node.js бота
        subprocess.run(['npm', 'init', '-y'], check=True)
        subprocess.run(['npm', 'install', 'mineflayer'], check=True)
        logger.info("Node.js зависимости установлены")
    except:
        logger.warning("Node.js не найден, буду использовать Python")
        
        # Для Python бота
        subprocess.run(['pip3', 'install', 'quarry'], check=True)
        logger.info("Python зависимости установлены")

if __name__ == "__main__":
    logger.info("="*50)
    logger.info("ЗАПУСК MINECRAFT БОТА")
    logger.info(f"Сервер: {SERVER_IP}:{SERVER_PORT}")
    logger.info(f"Бот: {BOT_USERNAME}")
    logger.info(f"Пароль: {BOT_PASSWORD}")
    logger.info("="*50)
    
    # Устанавливаем зависимости
    install_dependencies()
    
    # Запускаем бота
    bot = MinecraftBot()
    
    try:
        bot.connect()
        bot.monitor()
    except KeyboardInterrupt:
        logger.info("Остановка бота...")
        bot.stop()
        sys.exit(0)
