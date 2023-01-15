from aiohttp import web
from db import init_pg, close_pg
from models.users import create_user, email_exists, check_password
import bcrypt

routes = web.RouteTableDef()

@routes.post('/register')
async def register(request):
    try:
        data = await request.json()

        # Validate the user input
        if not "email" in data or not "password" in data:
            return web.json_response({"error": "Email and password are required."}, status=400)
        if len(data["password"]) < 8:
            return web.json_response({"error": "Password must be at least 8 characters."}, status=400)
        
        if await email_exists(request.app, data["email"]):
            return web.json_response({"error": "Email address already exists."}, status=400)

        await create_user(request.app, data["email"], data["password"])

        # # Send a confirmation email or message to the user
        # # ...
    except Exception as e:
        return web.json_response({"error": str(e)}, status=500)

    return web.json_response({"message": "User registered successfully."}, status=201)

@routes.post('/login')
async def login(request):
    try:
        data = await request.json()

        # Validate the user input
        if not "email" in data or not "password" in data:
            return web.json_response({"error": "Email and password are required."}, status=400)
        
        if not await email_exists(request.app, data["email"]):
            return web.json_response({"error": "Email address does not exist."}, status=400)

        if not await check_password(request.app, data["email"], data["password"]):
            return web.json_response({"error": "Incorrect password."}, status=400)

        # # Generate a JWT token for the user
        # # ...
    except Exception as e:
        return web.json_response({"error": str(e)}, status=500)

    return web.json_response({"message": "User logged in successfully."}, status=200)

app = web.Application()
app.on_startup.append(init_pg)
app.on_cleanup.append(close_pg)
app.add_routes(routes)
web.run_app(app)
