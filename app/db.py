import asyncpgsa
from asyncpgsa.connection import get_dialect
import json
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP, TEXT, JSONB
from sqlalchemy import MetaData, Table, Column, func


async def db():
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
    return db_


def table():
    metadata = MetaData()
    return Table('task1', metadata,
                 Column('id', UUID(), primary_key=True, nullable=False, default=func.gen_random_uuid()),
                 Column('label', TEXT(), nullable=True),
                 Column('data', JSONB(), nullable=True),
                 Column('created', TIMESTAMP(), nullable=False, default=func.NOW()),
                 Column('updated', TIMESTAMP(), nullable=False, default=func.NOW())
                 )


async def get_from_table(uuid):
    query = table.get().select().where(table.get().c.id == uuid)
    async with db.get().transaction() as conn:
        return await conn.fetchrow(query)


async def list_from_table(page, record_per_page=10):
    query = table().select().offset(page * record_per_page).limit((page + 1) * record_per_page)
    async with db().transaction() as conn:
        return await conn.fetch(query)


async def delete_from_table(uuid):
    query = table.get().delete().where(table.get().c.id == uuid)
    async with db.get().transaction() as conn:
        return await conn.fetch(query)


async def update_in_table():
    pass


async def add_in_table():
    pass
