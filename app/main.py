from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from app.db.session import init_db, close_db
from app.api import router  # Import the router from the single api.py file

app = FastAPI()

# Include the router defined in api.py
app.include_router(router)

@app.on_event("startup")
async def startup():
    await init_db()

@app.on_event("shutdown")
async def shutdown():
    await close_db()

# Register Tortoise ORM with FastAPI
register_tortoise(
    app,
    db_url="sqlite://market_place.sqlite3",  # Ensure this is your actual DB connection string
    modules={"models": ["app.models"]},  # Register models here
    generate_schemas=True,  # Generate schemas automatically
    add_exception_handlers=True,  # Add exception handlers for Tortoise ORM
)
