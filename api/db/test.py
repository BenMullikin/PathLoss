import asyncio
from session import engine
from sqlalchemy import text


async def test():
    async with engine.connect() as conn:
        result = await conn.execute(text("SELECT version();"))
        print(result.fetchone())


asyncio.run(test())
