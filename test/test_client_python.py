import aiohttp_rpc
import asyncio


async def run():
    async with aiohttp_rpc.WsJsonRpcClient('http://0.0.0.0:8080/rpc') as rpc:
        result = await rpc.add(label='TEST', data=[1, 2, 3, 4])
        print('1', result)
        print('2', await rpc.get(uuid=result))
        print('3',await rpc.update(uuid=result,data=[1,2,3,4,5]))
        print('4', await rpc.list(page=1))
        print('5', await rpc.delete(uuid=result))
loop = asyncio.get_event_loop()
loop.run_until_complete(run())
