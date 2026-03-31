from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
import asyncio

from app.constants.roles import Role
from app.core.config import settings
from app.db.session import AsyncSessionLocal
from app.models.user import User
from app.utils.password_helper import hash_password


async def seed_admin() -> None:
    email = settings.DEFAULT_ADMIN_EMAIL
    password = settings.DEFAULT_ADMIN_PASSWORD
    name = settings.DEFAULT_ADMIN_NAME

    if not email or not password or not name:
        raise ValueError("DEFAULT_ADMIN_EMAIL, DEFAULT_ADMIN_PASSWORD,and DEFAULT_ADMIN_NAME are required.")

    async with AsyncSessionLocal() as session:
        existing_user = await session.scalar(
            select(User).where(User.email == email)
        )

        if existing_user is not None:
            print(f"Admin already exists for email: {email}")
            return

        try:
            session.add(
                User(
                    email=email,
                    name=name,
                    role=Role.ADMIN,
                    password_hash=hash_password(password)
                )
            )
            await session.commit()
            print(f"Admin created successfully: {email}")
        except IntegrityError:
            await session.rollback()
            print(f"Admin already exists for email: {email}")


if __name__ == "__main__":
    asyncio.run(seed_admin())
