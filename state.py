import redis

async def init_state(app):
    app['state'] = redis.Redis(host='localhost', port=6379, db=0)