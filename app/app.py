from aiohttp import web
from .view.frontend import index_handler
from .rpc import create_rpc_server
from .db import db_create


async def create_app():
    """Run for create main app"""
    app = web.Application()
    rpc_server = create_rpc_server()
    app.router.add_routes([
        web.get('/rpc', rpc_server.handle_http_request),
        web.get('/', index_handler)
    ])
    app.on_shutdown.append(rpc_server.on_shutdown)
    await db_create()
    return app
