from aiohttp import web
from view.frontend import index_handler
from rpc import create_rpc_server


async def create_app():
    """Run for create main app"""
    app = web.Application()
    rpc_server = create_rpc_server()
    add_route(app, rpc_server)
    app.on_shutdown.append(rpc_server.on_shutdown)
    app.on_startup.append(on_start)
    return app


async def add_route(app, rpc_server):
    app.router.add_routes([
        web.get('/rpc', rpc_server.handle_http_request),
        web.get('/', index_handler)
    ])


async def on_start(app):
    """Run before app start"""
    pass
