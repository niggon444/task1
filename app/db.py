import asyncpgsa
from asyncpgsa.connection import get_dialect
import json
from sqlalchemy.sql import compiler
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP, TEXT, JSONB
from sqlalchemy import MetaData, Table, Column, func, dialects
from contextvars import ContextVar
from . import settings
db_var = ContextVar('db')
table_var = ContextVar('table')


async def db_create():
    """Create db pool and Create Table for SQSAlchemy Core"""
    dialect = get_dialect(
        json_serializer=json.dumps,
        json_deserializer=json.loads
    )
    db_ = await asyncpgsa.create_pool(
        host=settings.host_db,
        port=settings.port_db,
        database=settings.database_db,
        user=settings.user_db,
        dialect=dialect,
        password=settings.password_db
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
    query = table.select().offset(page * record_per_page).limit(record_per_page)
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
    table = table_var.get()
    data = json.dumps(data)
    query = table.update(values={'data': data, 'updated': func.NOW()}).where(table.c.id == uuid)
    query.parameters = {'data': data, 'updated': func.NOW()}
    async with db.acquire() as conn:
        await conn.fetchrow(query)
        return await conn.fetchrow(table.select().where(table.c.id == uuid))


async def add_in_table(label, data):
    db = db_var.get()
    table = table_var.get()
    query = table.insert(values=[{'label': label, 'data': data}])
    query.parameters = {'label': label, 'data': data}
    async with db.transaction() as conn:
        await conn.fetchrow(query)
        result = await conn.fetchrow(table.select().order_by(table.c.created.desc()))
        return str(result['id']).replace("UUID'", '').replace("'", '')
