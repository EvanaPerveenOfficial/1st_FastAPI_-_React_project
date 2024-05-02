import asyncio
import cProfile
import os
import pstats

from app.database import get_db
from app.routers import auth_user


async def profiled_code():
    db = next(get_db())

    await auth_user.create_user(
        email="tst7@example.com", password="password", role="user", db=db
    )
    await auth_user.get_user(id=1, db=db)

    auth_user.login(email="admin@gmail.com", password="1234", db=db)


def profile_auth_user():
    profiler = cProfile.Profile()

    profiler.runctx("asyncio.run(profiled_code())", globals(), locals())

    file_path = "profiler_stats.txt"

    with open(file_path, "w") as f:
        stats = pstats.Stats(profiler, stream=f)
        stats.print_stats()


profile_auth_user()
