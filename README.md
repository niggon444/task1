На aiohttp сделай приложение с RPC запросами (get, add, delete, list, update)

Для подключение к базе возьми asyncpgsa 

Для запросов в базу возьми sqlalchemy core

В базе будет 1 таблица:
Id - uuid
label - text
data - jsonb 
created - timestamp
updated - timestamp

При создании запиши на вход приходит label и data, id генерируется на уровне базы, created проставляется автоматически как и updated, updated всегда меняется при обновлении данных

Метод list должен иметь пагинацию 
