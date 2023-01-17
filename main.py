import asyncio

from aiohttp import web
from dotenv import load_dotenv
from db import init_pg, close_pg
from models.user import create_user, email_exists, check_password, find_user_id
from models.session import create_session
from state import init_state
from auth import verify_token, create_token

routes = web.RouteTableDef()

@routes.post('/register')
async def register(request):
    try:
        data = await request.json()
        email = data.get("email")
        password = data.get("password")

        # Validate the user input
        if email is None or password is None:
            return web.json_response({"error": "Email and password are required."}, status=400)
        if len(password) < 8:
            return web.json_response({"error": "Password must be at least 8 characters."}, status=400)
        
        if await email_exists(request.app, email):
            return web.json_response({"error": "Email address already exists."}, status=400)

        await create_user(request.app, email, password)

        # # Send a confirmation email or message to the user
        # # ...
    except Exception as e:
        return web.json_response({"error": str(e)}, status=500)

    return web.json_response({"message": "User registered successfully."}, status=201)

@routes.post('/login')
async def login(request):
    try:
        data = await request.json()
        email = data.get("email")
        password = data.get("password")

        # Validate the user input
        if email is None or password is None:
            return web.json_response({"error": "Email and password are required."}, status=400)
        
        if not await email_exists(request.app, email):
            return web.json_response({"error": "Email address does not exist."}, status=400)

        if not await check_password(request.app, email, password):
            return web.json_response({"error": "Incorrect password."}, status=400)

        user_id = await find_user_id(request.app, email)

        token = create_token(user_id)

        return web.json_response({"token": token}, status=200)
        

    except Exception as e:
        return web.json_response({"error": str(e)}, status=500)

PREFIX = 'Bearer '

def get_token(header):
    if not header.startswith(PREFIX):
        raise ValueError('Invalid token')

    return header[len(PREFIX):]

@routes.get('/protected')
async def protected(request):
    try:
        token = get_token(request.headers.get("Authorization"))
        if token is None:
            return web.json_response({"error": "Authorization header is required."}, status=400)
        
        user_id = verify_token(token)

        print(user_id)

        # Do something with the user id
        # ...

    except Exception as e:
        return web.json_response({"error": str(e)}, status=500)

    return web.json_response({"message": "You are authorized."}, status=200)

def main():
    loop = asyncio.get_event_loop()
    load_dotenv()
    app = web.Application()
    app.on_startup.append(init_pg)
    app.on_cleanup.append(close_pg)
    app.on_startup.append(init_state)
    app.add_routes(routes)
    web.run_app(app, port=8080)

if __name__ == '__main__':
    main()