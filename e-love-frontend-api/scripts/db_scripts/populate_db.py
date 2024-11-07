# populate_db.py

import asyncio
import random
import uuid
from contextlib import asynccontextmanager

from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession

from configuration.database import AsyncSessionLocal
from core.db.models.categories.categories import Categories
from core.db.models.intermediate_models.posts_categories import posts_categories_table
from core.db.models.intermediate_models.user_categories import user_categories_table
from core.db.models.intermediate_models.user_genders import user_genders_table
from core.db.models.intermediate_models.user_roles import user_roles_table
from core.db.models.posts.user_post import UserPost
from core.db.models.users.user_gender import UserGender
from core.db.models.users.user_role import UserRole
from core.db.models.users.user_status import UserStatus
from core.db.models.users.user_interaction import UserInteraction
from core.db.models.users.users import User

SEED = 12345
random.seed(SEED)
fake = Faker()
fake.seed_instance(SEED)


@asynccontextmanager
async def get_db_session() -> AsyncSession:
    """
    Асинхронный контекстный менеджер для получения сессии базы данных.

    :yield: Асинхронная сессия базы данных.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            print(f"Database session error: {e}")
            raise


def deterministic_uuid(name: str) -> str:
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, name))


async def populate_user_statuses(db_session: AsyncSession):
    """
    Заполняет таблицу UserStatus предопределёнными статусами пользователей.

    :param db_session: Сессия базы данных.
    :return: Список созданных объектов UserStatus.
    """
    statuses = ["Active", "Inactive", "Banned"]
    status_objects = []
    for status in statuses:
        status_obj = UserStatus(id=deterministic_uuid(f"user_status_{status}"), status_name=status)
        db_session.add(status_obj)
        status_objects.append(status_obj)
    await db_session.commit()
    return status_objects


async def populate_user_genders(db_session: AsyncSession):
    """
    Заполняет таблицу UserGender предопределёнными полами пользователей.

    :param db_session: Сессия базы данных.
    :return: Список созданных объектов UserGender.
    """
    genders = ["Male", "Female", "Other"]
    gender_objects = []
    for gender in genders:
        gender_obj = UserGender(id=deterministic_uuid(f"user_gender_{gender}"), gender_name=gender)
        db_session.add(gender_obj)
        gender_objects.append(gender_obj)
    await db_session.commit()
    return gender_objects


async def populate_categories(db_session: AsyncSession):
    """
    Заполняет таблицу Categories предопределёнными категориями.

    :param db_session: Сессия базы данных.
    :return: Список созданных объектов Categories.
    """
    categories_list = [
        "Music",
        "Sports",
        "Travel",
        "Technology",
        "Art",
        "Food",
        "Health",
        "Education",
        "Business",
        "Entertainment",
        "Science",
        "Fashion",
        "Politics",
        "History",
        "Nature",
        "Movies",
        "Books",
        "Gaming",
        "Photography",
        "Animals",
    ]
    category_objects = []
    for category in categories_list:
        category_obj = Categories(
            id=deterministic_uuid(f"category_{category}"),
            category_name=category,
            category_descr=fake.text(max_nb_chars=200),
            category_icon=fake.word(),
        )
        db_session.add(category_obj)
        category_objects.append(category_obj)
    await db_session.commit()
    return category_objects


async def populate_user_roles(db_session: AsyncSession):
    """
    Заполняет таблицу UserRole предопределёнными ролями пользователей.

    :param db_session: Сессия базы данных.
    :return: Список созданных объектов UserRole.
    """
    roles = ["Admin", "User", "Moderator"]
    role_objects = []
    for role in roles:
        role_obj = UserRole(id=deterministic_uuid(f"user_role_{role}"), role_name=role)
        db_session.add(role_obj)
        role_objects.append(role_obj)
    await db_session.commit()
    return role_objects


async def populate_users(db_session: AsyncSession, statuses, num_users=500):
    """
    Создаёт и добавляет в базу данных случайных пользователей.

    :param db_session: Сессия базы данных.
    :param statuses: Список объектов UserStatus.
    :param num_users: Количество пользователей для создания.
    :return: Список созданных объектов User.
    """
    user_objects = []
    for i in range(num_users):
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = f"user{i}@example.com"
        user_id = deterministic_uuid(f"user_{i}")
        user = User(
            id=user_id,
            first_name=first_name,
            last_name=last_name,
            user_descr=fake.text(max_nb_chars=200),
            email=email,
            password_hash=fake.sha256(),
            status_id=random.choice(statuses).id,
            created_at=fake.date_time_between(start_date="-2y", end_date="now"),
            updated_at=fake.date_time_between(start_date="-2y", end_date="now"),
        )
        db_session.add(user)
        user_objects.append(user)
    await db_session.commit()
    return user_objects


async def assign_roles_to_users(db_session: AsyncSession, users, roles):
    """
    Назначает фиксированные роли пользователям.

    :param db_session: Сессия базы данных.
    :param users: Список объектов User.
    :param roles: Список объектов UserRole.
    """
    for i, user in enumerate(users):
        # Назначаем роли на основе индекса пользователя
        assigned_roles = [roles[i % len(roles)]]
        for role in assigned_roles:
            association = user_roles_table.insert().values(user_id=user.id, role_id=role.id)
            await db_session.execute(association)
    await db_session.commit()


async def assign_categories_to_users(db_session: AsyncSession, users, categories):
    """
    Назначает фиксированные категории пользователям.

    :param db_session: Сессия базы данных.
    :param users: Список объектов User.
    :param categories: Список объектов Categories.
    """
    for i, user in enumerate(users):
        # Назначаем категории на основе индекса пользователя
        assigned_categories = categories[i % len(categories) : (i % len(categories)) + 3]
        for category in assigned_categories:
            association = user_categories_table.insert().values(
                user_id=user.id, category_id=category.id
            )
            await db_session.execute(association)
    await db_session.commit()


async def assign_genders_to_users(db_session: AsyncSession, users, genders):
    """
    Назначает пол каждому пользователю.

    :param db_session: Сессия базы данных.
    :param users: Список объектов User.
    :param genders: Список объектов UserGender.
    """
    for i, user in enumerate(users):
        gender = genders[i % len(genders)]
        association = user_genders_table.insert().values(user_id=user.id, gender_id=gender.id)
        await db_session.execute(association)
    await db_session.commit()


async def populate_user_posts(db_session: AsyncSession, users):
    """
    Создаёт и добавляет в базу данных посты пользователей.

    :param db_session: Сессия базы данных.
    :param users: Список объектов User.
    :return: Список созданных объектов UserPost.
    """
    post_objects = []
    for i, user in enumerate(users):
        num_posts = 3  # Фиксированное количество постов
        for j in range(num_posts):
            post_id = deterministic_uuid(f"post_{i}_{j}")
            post = UserPost(
                id=post_id,
                post_title=fake.sentence(nb_words=6),
                post_descr=fake.text(max_nb_chars=500),
                user_id=user.id,
                created_at=fake.date_time_between(start_date="-2y", end_date="now"),
                updated_at=fake.date_time_between(start_date="-2y", end_date="now"),
            )
            db_session.add(post)
            post_objects.append(post)
    await db_session.commit()
    return post_objects


async def assign_categories_to_posts(db_session: AsyncSession, posts, categories):
    """
    Назначает фиксированные категории постам.

    :param db_session: Сессия базы данных.
    :param posts: Список объектов UserPost.
    :param categories: Список объектов Categories.
    """
    for i, post in enumerate(posts):
        assigned_categories = categories[i % len(categories) : (i % len(categories)) + 2]
        for category in assigned_categories:
            association = posts_categories_table.insert().values(
                post_id=post.id, category_id=category.id
            )
            await db_session.execute(association)
    await db_session.commit()


async def populate_user_interactions(db_session: AsyncSession, users):
    """
    Создаёт и добавляет в базу данных взаимодействия между пользователями.

    :param db_session: Сессия базы данных.
    :param users: Список объектов User.
    """
    interaction_types = ["MATCH", "REJECT"]
    user_ids = [user.id for user in users]

    interaction_objects = []
    for user in users:
        # Выбираем случайное количество взаимодействий для каждого пользователя
        num_interactions = random.randint(5, 15)
        # Получаем список возможных целевых пользователей (исключая самого себя)
        possible_targets = [uid for uid in user_ids if uid != user.id]
        # Выбираем случайных целевых пользователей
        target_user_ids = random.sample(
            possible_targets, min(num_interactions, len(possible_targets))
        )

        for target_user_id in target_user_ids:
            interaction = UserInteraction(
                user_id=user.id,
                target_user_id=target_user_id,
                interaction_type=random.choice(interaction_types),
            )
            db_session.add(interaction)
            interaction_objects.append(interaction)
    await db_session.commit()
    return interaction_objects


async def main():
    """
    Основная функция скрипта для заполнения базы данных.
    """
    async with get_db_session() as db_session:
        try:
            print("Populating user_status...")
            statuses = await populate_user_statuses(db_session)

            print("Populating user_gender...")
            genders = await populate_user_genders(db_session)

            print("Populating categories...")
            categories = await populate_categories(db_session)

            print("Populating user_role...")
            roles = await populate_user_roles(db_session)

            print("Users creation...")
            users = await populate_users(db_session, statuses, num_users=500)

            print("Assigning roles to the users...")
            await assign_roles_to_users(db_session, users, roles)

            print("Assigning categories to the users...")
            await assign_categories_to_users(db_session, users, categories)

            print("Assigning genders to the users...")
            await assign_genders_to_users(db_session, users, genders)

            print("Users posts creation...")
            posts = await populate_user_posts(db_session, users)

            print("Assigning categories to the posts...")
            await assign_categories_to_posts(db_session, posts, categories)

            print("Populating user interactions...")
            await populate_user_interactions(db_session, users)

            print("Database has been successfully populated with consistent data.")
        except Exception as e:
            print(f"Exception: {e}")
            await db_session.rollback()


if __name__ == "__main__":
    asyncio.run(main())
