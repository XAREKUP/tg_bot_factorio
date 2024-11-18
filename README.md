# tg_bot_factorio
tg_bot_factorio — это проект, созданный для запуска сервера Factorio на операционной системе Linux в качестве пользовательской службы systemd. Кроме того, он устанавливает Telegram-бота, который обеспечивает удобное управление сервером, а также позволяет отправлять команды на консоль сервера с помощью протокола RCON.


# Установка
- Клонируйте этот репозиторий на машину, где будет хостится сервер и бот.
- Запустите скрипт `script_install.sh`
- Введите зарпашиваемые данные. Среди них есть токен телеграмм бота. Его можно получить, создав нового бота или сгенерировав новый токен у [BotFather](https://telegram.me/BotFather).
- Для запуска бота запустите скрипт `start_bot.sh`
- Бот работает и принимает команды через телеграм.
- Если необходимо изменить введенный ранее параметр, то отредактируйте файл data/parameters.txt

# Команды для управления сервером

`/start_server` - запускает сервер  
`/stop_server` - останавливает сервер  
`/status_server` - выводит статус сервер  

# Команды `RCON`  для отправки сообщений на сервер `Factorio`

`/send_text` - отправляет сообщение на сервер  
`/players` - выводит игроков на сервере    
`/server-save` - сервер выполняет сохранение мира    
