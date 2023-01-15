import aiopg

dsn = "dbname=mydb user=admin password=admin host=localhost port=5432"

async def init_pg(app):
    app['db'] = await aiopg.create_pool(dsn)

async def close_pg(app):
    app['db'].close()
    await app['db'].wait_closed()