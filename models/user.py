import bcrypt

async def create_user(app, email, password):
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    async with app['db'].acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("INSERT INTO tutors (email, password) VALUES (%s, %s)", (email, hashed_password))

async def email_exists(app, email):
    async with app['db'].acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("SELECT 1 FROM tutors WHERE email = %s", (email,))
            return await cur.fetchone() is not None

async def check_password(app, email, password):
    async with app['db'].acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("SELECT password FROM tutors WHERE email = %s", (email,))
            result = await cur.fetchone()
    if result is None:
        return False
    db_password = result[0]

    return bcrypt.checkpw(password.encode(), bytes.fromhex(db_password[2:]))

async def find_user_id(app, email):
    async with app['db'].acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("SELECT * FROM tutors WHERE email = %s", (email,))
            result = await cur.fetchone()
    if result is None:
        return None
    return result[0]
