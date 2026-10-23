import aiohttp
import asyncio
from sqlalchemy import insert
from database import SessionLocal, engine, Base
from models import Post

API_URL = "https://jsonplaceholder.typicode.com/posts"

async def obtener_posts():
    async with aiohttp.ClientSession() as session:
        async with session.get(API_URL) as resp:
            return await resp.json()

async def guardar_posts(posts):
    async with SessionLocal() as session:
        async with session.begin():
            for p in posts:
                stmt = insert(Post).values(
                    id=p["id"],
                    user_id=p["userId"],
                    title=p["title"],
                    body=p["body"]
                )
                await session.execute(stmt)

async def main():
    # Crear tablas si no existen
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    print("Obteniendo datos de la API...")
    posts = await obtener_posts()

    print(f"Se recibieron {len(posts)} posts. Guardando en la base...")
    await guardar_posts(posts)

    print("Proceso completado.")

if __name__ == "__main__":
    asyncio.run(main())
