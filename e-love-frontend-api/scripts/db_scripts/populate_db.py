import uuid

from faker import Faker

from configuration.database import get_db_session

# Import models and intermediate tables
from core.db.models.categories.categories import Categories
from core.db.models.intermediate_models.posts_categories import posts_categories_table
from core.db.models.intermediate_models.user_categories import user_categories_table
from core.db.models.intermediate_models.user_genders import user_genders_table
from core.db.models.intermediate_models.user_roles import user_roles_table
from core.db.models.posts.user_post import UserPost
from core.db.models.users.user_gender import UserGender
from core.db.models.users.user_role import UserRole
from core.db.models.users.user_status import UserStatus
from core.db.models.users.users import User

fake = Faker()

# Population of "support" tables


def populate_user_statuses(db_session):
    statuses = ["Active", "Inactive", "Banned"]
    status_objects = []
    for status in statuses:
        status_obj = UserStatus(id=str(uuid.uuid4()), status_name=status)
        db_session.add(status_obj)
        status_objects.append(status_obj)
    db_session.commit()
    return status_objects


def populate_user_genders(db_session):
    genders = ["Male", "Female", "Other"]
    gender_objects = []
    for gender in genders:
        gender_obj = UserGender(id=str(uuid.uuid4()), gender_name=gender)
        db_session.add(gender_obj)
        gender_objects.append(gender_obj)
    db_session.commit()
    return gender_objects


def populate_categories(db_session):
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
            id=str(uuid.uuid4()),
            category_name=category,
            category_descr=fake.text(max_nb_chars=200),
            category_icon=fake.word(),
        )
        db_session.add(category_obj)
        category_objects.append(category_obj)
    db_session.commit()
    return category_objects


def populate_user_roles(db_session):
    roles = ["Admin", "User", "Moderator"]
    role_objects = []
    for role in roles:
        role_obj = UserRole(id=str(uuid.uuid4()), role_name=role)
        db_session.add(role_obj)
        role_objects.append(role_obj)
    db_session.commit()
    return role_objects


# Population of main tables


def populate_users(db_session, statuses, num_users=500):
    user_objects = []
    for _ in range(num_users):
        user = User(
            id=str(uuid.uuid4()),
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            user_descr=fake.text(max_nb_chars=200),
            email=fake.unique.email(),
            password_hash=fake.sha256(),
            status_id=fake.random_element(elements=[status.id for status in statuses]),
            created_at=fake.date_time_between(start_date="-2y", end_date="now"),
            updated_at=fake.date_time_between(start_date="-2y", end_date="now"),
        )
        db_session.add(user)
        user_objects.append(user)
    db_session.commit()
    return user_objects


# Population of intermediate tables


def assign_roles_to_users(db_session, users, roles):
    for user in users:
        num_roles = fake.random_int(min=1, max=2)
        user_roles_sample = fake.random_elements(elements=roles, length=num_roles, unique=True)
        for role in user_roles_sample:
            association = user_roles_table.insert().values(user_id=user.id, role_id=role.id)
            db_session.execute(association)
    db_session.commit()


def assign_categories_to_users(db_session, users, categories):
    for user in users:
        num_categories = fake.random_int(min=1, max=5)
        user_categories_sample = fake.random_elements(
            elements=categories, length=num_categories, unique=True
        )
        for category in user_categories_sample:
            association = user_categories_table.insert().values(
                user_id=user.id, category_id=category.id
            )
            db_session.execute(association)
    db_session.commit()


def assign_genders_to_users(db_session, users, genders):
    for user in users:
        num_genders = 1
        user_genders_sample = fake.random_elements(
            elements=genders, length=num_genders, unique=True
        )
        for gender in user_genders_sample:
            association = user_genders_table.insert().values(user_id=user.id, gender_id=gender.id)
            db_session.execute(association)
    db_session.commit()


def populate_user_posts(db_session, users):
    post_objects = []
    for user in users:
        num_posts = fake.random_int(min=1, max=5)
        for _ in range(num_posts):
            post = UserPost(
                id=str(uuid.uuid4()),
                post_title=fake.sentence(nb_words=6),
                post_descr=fake.text(max_nb_chars=500),
                user_id=user.id,
                created_at=fake.date_time_between(start_date="-2y", end_date="now"),
                updated_at=fake.date_time_between(start_date="-2y", end_date="now"),
            )
            db_session.add(post)
            post_objects.append(post)
    db_session.commit()
    return post_objects


def assign_categories_to_posts(db_session, posts, categories):
    for post in posts:
        num_categories = fake.random_int(min=1, max=3)
        post_categories_sample = fake.random_elements(
            elements=categories, length=num_categories, unique=True
        )
        for category in post_categories_sample:
            association = posts_categories_table.insert().values(
                post_id=post.id, category_id=category.id
            )
            db_session.execute(association)
    db_session.commit()


def main():
    with get_db_session() as db_session:
        try:
            print("Populating user_status...")
            statuses = populate_user_statuses(db_session)

            print("Populating user_gender...")
            genders = populate_user_genders(db_session)

            print("Populating categories...")
            categories = populate_categories(db_session)

            print("Populating user_role...")
            roles = populate_user_roles(db_session)

            print("Users creation...")
            users = populate_users(db_session, statuses, num_users=500)

            print("Assigning roles to the users...")
            assign_roles_to_users(db_session, users, roles)

            print("Assigning categories to the users...")
            assign_categories_to_users(db_session, users, categories)

            print("Assigning genders to the users...")
            assign_genders_to_users(db_session, users, genders)

            print("Users posts creation...")
            posts = populate_user_posts(db_session, users)

            print("Assigning categories to the posts...")
            assign_categories_to_posts(db_session, posts, categories)

            print("Database has been successfully populated with random rows.")
        except Exception as e:
            print(f"Exception: {e}")
            db_session.rollback()


if __name__ == "__main__":
    main()
