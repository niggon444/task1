import aiohttp_rpc


def create_rpc_server():
    """Run for create rpc_server"""
    rpc_server = aiohttp_rpc.WsJsonRpcServer()
    rpc_server.add_methods([get, add, list, update, delete])
    return rpc_server

def get():
    pass


def add():
    pass


def list():
    pass


def update():
    pass


def delete():
    pass
