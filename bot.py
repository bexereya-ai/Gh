const mineflayer = require('mineflayer');

const SERVER_IP = "RexWorld.aternos.me";
const SERVER_PORT = 28068;
const BOT_USERNAME = "IrnaMoret345";
const BOT_PASSWORD = "uiop0035";

console.log('='.repeat(50));
console.log('🤖 MINECRAFT БОТ ДЛЯ FLY.IO');
console.log(`Сервер: ${SERVER_IP}:${SERVER_PORT}`);
console.log(`Бот: ${BOT_USERNAME}`);
console.log('='.repeat(50));

function createBot() {
    console.log('🔄 Подключение к серверу...');
    
    const bot = mineflayer.createBot({
        host: SERVER_IP,
        port: SERVER_PORT,
        username: BOT_USERNAME,
        version: '1.16.5' // Укажи версию своего сервера
    });

    bot.on('login', () => {
        console.log('✅ Бот зашел на сервер!');
        
        // Отправляем команды регистрации и входа
        setTimeout(() => {
            bot.chat(`/register ${BOT_PASSWORD}`);
            console.log('📝 Отправлена команда: /register');
        }, 3000);
        
        setTimeout(() => {
            bot.chat(`/login ${BOT_PASSWORD}`);
            console.log('🔑 Отправлена команда: /login');
        }, 4000);
    });

    // Прыжки каждые 3 минуты
    setInterval(() => {
        bot.setControlState('jump', true);
        setTimeout(() => bot.setControlState('jump', false), 500);
        console.log('🦘 Бот прыгнул (keep-alive)');
    }, 180000);

    // Обработка отключения
    bot.on('end', (reason) => {
        console.log('❌ Бот отключен:', reason);
        console.log('🔄 Переподключение через 10 секунд...');
        setTimeout(createBot, 10000);
    });

    bot.on('error', (err) => {
        console.log('⚠️ Ошибка:', err.message);
    });

    bot.on('kicked', (reason) => {
        console.log('👢 Бот кикнут:', reason);
        console.log('🔄 Переподключение через 10 секунд...');
        setTimeout(createBot, 10000);
    });

    // Проверка соединения
    setInterval(() => {
        if (!bot.entity) {
            console.log('⚠️ Потеряно соединение с сервером');
        }
    }, 30000);
}

// Запускаем бота
createBot();

// Обработка сигналов остановки
process.on('SIGINT', () => {
    console.log('👋 Бот остановлен');
    process.exit(0);
});
