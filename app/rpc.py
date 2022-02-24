import aiohttp_rpc
import db


def create_rpc_server():
    """Run for create rpc_server"""
    rpc_server = aiohttp_rpc.WsJsonRpcServer()
    rpc_server.add_methods([get, add, list, update, delete])
    return rpc_server


async def get(uuid):
    return await db.get_from_table(uuid)


async def add(label, data):
    return await db.add_in_table(label, data)


async def list():
    return await db.add_in_table(label, data)


async def update(uuid, data):
    return await db.update_in_table(uuid, data)


async def delete(uuid):
    return await db.delete_from_table(uuid)
