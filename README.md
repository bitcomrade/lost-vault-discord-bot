# Lost Vault RPG discord bot

Discord bot for a mobile game called Lost Vault: Idle Retro RPG by Vaultomb.

https://lost-vault.com/

Lost Vault has an API site with information, parameters and attributes of players and tribes (guilds).
My bot listens for keywords in the discord channel and sends a request to API site, parses recieved HTML code with BeatufulSoup and returns to user in a readable form with a help of tabulate module.

Available commands:
```
!hello - greetings message
!seekhelp - help and instructions
!помоги - help and instructions in Russian
!seekplayer {Name} - searches for a player
!seektribe {Name} - searches for a tribe
```
Bot is up and running on herokuapp server with bot tokken placed in herokuapp config vars. to run on other servers, you may need to edit line 48 in ```main.py``` and also create an ```.env``` file.

----

Discord бот для мобильной игры Lost Vault: Idle Retro RPG от Vaultomb.

https://lost-vault.com/

У Lost Vault есть API сайт с информацией, параметрами и атрибутами игроков и племен (гильдий).
Мой бот отслеживает ключевые слова в канале discord и отправляет запрос на API сайт, парсит полученный HTML код с помощью BeatufulSoup и возвращает пользователю в читабельном виде с помощью модуля tabulate.

Доступные команды:
```
!hello - приветствие
!seekhelp - помощь и инструкции
!помоги - помощь и инструкции на русском языке
!seekplayer {Имя} - поиск игрока
!seektribe {Имя} - поиск племени
```
Бот запущен на сервере herokuapp с токеном бота, размещенным в конфигах herokuapp. Для запуска на других серверах, возможно, потребуется отредактировать строку 48 в ``main.py``, а также создать файл ``.env``.
