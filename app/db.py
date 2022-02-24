import asyncpgsa
from asyncpgsa.connection import get_dialect
import json
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP, TEXT, JSONB
from sqlalchemy import MetaData, Table, Column, func
from contextvars import ContextVar
db_var = ContextVar('db')
table_var = ContextVar('table')
async def db_create():

    dialect = get_dialect(
        json_serializer=json.dumps,
        json_deserializer=json.loads
    )
    db_ = await asyncpgsa.create_pool(
        host='127.0.0.1',
        port=5432,
        database='task1',
        user='postgres',
        dialect=dialect,
        password='1234'
    )
    db_var.set(db_)
    metadata = MetaData()
    table_var.set(Table('task1', metadata,
                 Column('id', UUID(), primary_key=True, nullable=False, default=func.gen_random_uuid()),
                 Column('label', TEXT(), nullable=True),
                 Column('data', JSONB(), nullable=True),
                 Column('created', TIMESTAMP(), nullable=False, default=func.NOW()),
                 Column('updated', TIMESTAMP(), nullable=False, default=func.NOW())
                 ))
    return db_


async def get_from_table(uuid):
    table = table_var.get()
    db = db_var.get()
    query = table.select().where(table.c.id == uuid)
    async with db.transaction() as conn:
        return await conn.fetchrow(query)


async def list_from_table(page, record_per_page=10):
    table = table_var.get()
    db = db_var.get()
    query = table.select().offset(page * record_per_page).limit((page + 1) * record_per_page)
    async with db.transaction() as conn:
        return await conn.fetch(query)


async def delete_from_table(uuid):
    table = table_var.get()
    db = db_var.get()
    query = table.delete().where(table.c.id == uuid)

    async with db.transaction() as conn:
        return await conn.fetch(query)


async def update_in_table(uuid, data):
    db = db_var.get()
    #query1 = table.get().update(table.get().c.id == uuid_).values([{'data': data_, 'updated': func.NOW()}])
    data = json.dumps(data)
    table = table_var.get()
    async with db.acquire() as conn:
        # return await conn.fetchrow(query1)
        await conn.fetchrow("UPDATE task1 SET updated = NOW() , data = $1  WHERE task1.id = $2", data, uuid)
        return await conn.fetchrow(table.select().where(table.c.id == uuid))


async def add_in_table(label, data):
    # query = table.get().insert().values({'label': label_, 'data': data_}) #тут должно быть так но оно не работает ошибка AttributeError: 'Insert' object has no attribute 'parameters'
    data = json.dumps(data)
    db = db_var.get()
    table = table_var.get()
    async with db.transaction() as conn:
        # return await conn.fetchrow(query)
        await conn.fetchrow("INSERT INTO task1(label,data) VALUES($1,$2)", label, data)
        result = await conn.fetchrow(table.select().order_by(table.c.created.desc()))
        return str(result['id']).replace("UUID'", '').replace("'", '')
