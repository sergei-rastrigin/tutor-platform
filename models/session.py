import uuid
import datetime

async def create_session(app, email):
    session_id = str(uuid.uuid4())
    ttl = datetime.timedelta(seconds=30)
    app['state'].hmset(session_id, {"user_id" : email})
    app['state'].expire(session_id, ttl)
    return session_id