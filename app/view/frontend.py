from aiohttp import web


def html_response(document):
    """Load file index.html"""
    s = open(document, "r")
    return web.Response(text=s.read(), content_type='text/html')


async def index_handler(request):
    """Response root requests"""
    return html_response('app/view/index.html')
