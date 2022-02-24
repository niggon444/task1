import aiohttp_rpc
from .db import *


def create_rpc_server():
    """Run for create rpc_server"""
    rpc_server = aiohttp_rpc.WsJsonRpcServer()
    rpc_server.add_methods([get, add, list, update, delete])
    return rpc_server


async def get(uuid):
    return await get_from_table(uuid)


async def add(label, data):
    return await add_in_table(label, data)


async def list(page, record_per_page=10):
    return await list_from_table(page, record_per_page)


async def update(uuid, data):
    return await update_in_table(uuid, data)


async def delete(uuid):
    return await delete_from_table(uuid)
