# Lost Vault RPG discord bot

Discord bot for a mobile game called Lost Vault: Idle Retro RPG by Vaultomb.

https://lost-vault.com/

Lost Vault has an API site with information, parameters and attributes of players and tribes (guilds).
My bot listens for keywords in the discord channel and sends a request to API site, parses recieved HTML code with BeatufulSoup and returns to user in a readable form with a help of tabulate module.

Available commands:
```
!hello - greetings message
!language en / !language ru - change messages language to English/Russian
!seekhelp - help and instructions
!player {Name} - searches for a player
!tribe {Name} - searches for a tribe
!players {Name1} && {Name2} - compares two players
!tribes {Tribe1} && {Tribe2} - compares two tribes
```
Bot is up and running on herokuapp server with bot token placed in herokuapp config vars. to run on other servers, you may need to edit line 11 in ```bot.py``` and also create an ```.env``` file.

----

Discord бот для мобильной игры Lost Vault: Idle Retro RPG от Vaultomb.

https://lost-vault.com/

У Lost Vault есть API сайт с информацией, параметрами и атрибутами игроков и племен (гильдий).
Мой бот отслеживает ключевые слова в канале discord и отправляет запрос на API сайт, парсит полученный HTML код с помощью BeatufulSoup и возвращает пользователю в читабельном виде с помощью модуля tabulate.

Доступные команды:
```
!hello - приветствие
!language en / !language ru - сменить язык сообщений на английский/русский
!seekhelp - помощь и инструкции
!player {Имя} - поиск игрока
!tribe {Имя} - поиск племени
!players {Имя1} && {Имя2} - сравнение двух игроков
!tribes {Племя1} && {Племя2} - сравнение двух племен
```
Бот запущен на сервере herokuapp с токеном бота, размещенным в конфигах herokuapp. Для запуска на других серверах, возможно, потребуется отредактировать строку 11 в ``bot.py``, а также создать файл ``.env``.
