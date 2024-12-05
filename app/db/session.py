from tortoise import Tortoise
import app.settings as settings

async def init_db():
    await Tortoise.init(
        db_url=settings.DATABASE_URL,
        modules={"models": ["app.models"]}
    )
    await Tortoise.generate_schemas()

async def close_db():
    await Tortoise.close_connections()




TORTOISE_ORM = {
    "connections": {
        "default": "sqlite://market_place.sqlite3",  # Use your actual DB URL
    },
    "apps": {
        "models": {
            "models": ["app.models", "aerich.models"],  # Include aerich models
            "default_connection": "default",
        }
    }
}