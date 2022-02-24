from app import app
from aiohttp import web

if __name__ == '__main__':
    app = app.create_app()
    web.run_app(app, host='0.0.0.0', port=8080)


