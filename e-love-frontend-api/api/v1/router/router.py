# app/api/v1/router/router.py
# pylint: disable-all
# type: ignore
from fastapi import APIRouter

from api.v1.endpoints.categories.categories import router as categories_router
from api.v1.endpoints.chat.chat import router as chat_router
from api.v1.endpoints.user_categories.user_categories import router as user_categories_router
from api.v1.endpoints.user_gender.user_gender import router as user_gender_router
from api.v1.endpoints.user_images.user_images import router as user_images_router
from api.v1.endpoints.user_interaction.user_interaction import router as user_interaction_router
from api.v1.endpoints.user_post.user_post import router as user_post_router
from api.v1.endpoints.user_role.user_role import router as user_role_router
from api.v1.endpoints.user_role_association.user_roles_association import (
    router as user_role_association_router,
)
from api.v1.endpoints.user_status.user_status import router as user_status_router
from api.v1.endpoints.users.users import router as users_router
from api.v1.endpoints.users_matching.users_matching import router as users_matching_router

api_router = APIRouter()
api_router.include_router(users_router, prefix="/api/v1", tags=["Users"])
api_router.include_router(user_role_router, prefix="/api/v1", tags=["User role"])
api_router.include_router(
    user_role_association_router, prefix="/api/v1", tags=["User role association"]
)
api_router.include_router(user_gender_router, prefix="/api/v1", tags=["User Gender"])
api_router.include_router(categories_router, prefix="/api/v1", tags=["Categories"])
api_router.include_router(user_status_router, prefix="/api/v1", tags=["User Status"])
api_router.include_router(user_post_router, prefix="/api/v1", tags=["User Post"])
api_router.include_router(user_categories_router, prefix="/api/v1", tags=["User Categories"])
api_router.include_router(chat_router, prefix="/chat/v1", tags=["Users chat"])
api_router.include_router(user_images_router, prefix="/api/v1", tags=["User Images"])

api_router.include_router(user_interaction_router, prefix="/api/v1", tags=["User interactions"])
api_router.include_router(
    users_matching_router,
    prefix="/api/v1",
    tags=["Users matching", "Matching", "Match", "User", "Users"],
)

# ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠿⠿⠿⠟⢿⣻⣟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢻⡝⠬⢋⣤⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢋⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣦⣄⡀⠀⠀⠀⠀⢀⠢⠑⡌⠲⣉
# ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢟⣫⣵⣶⣶⣿⣿⣿⣿⣟⡳⠶⣶⣬⣝⠻⣿⣿⢿⡿⠟⠿⡹⠓⢎⣡⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⣰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣤⡀⠀⠀⠀⠁⢀⠃⡐
# ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢛⣵⢞⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣭⡻⠿⣖⣩⣴⣶⣾⣶⣶⣾⣯⣝⣻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢡⣾⣿⣿⣿⣿⣿⣿⣿⡿⢟⣫⠐⠈⡀⠀⠀⠈⠉⠉⠛⠿⣿⣿⣿⣶⡀⠀⠀⠀⠀⠀
# ⣿⣿⣿⢯⢷⡙⣎⠷⣽⢾⡿⣟⢿⡽⡿⢋⡴⣯⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢟⣵⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⡻⣿⣿⣿⣿⣿⣿⣿⡿⠋⣴⣿⣿⣿⣿⠟⠛⠉⠘⠉⠐⠉⠙⠋⠑⣙⣶⠢⠐⠀⠀⠀⠀⠀⠙⠻⣿⣷⣄⡂⠀⠀⠀
# ⣿⡟⣏⢞⡢⡝⡜⢫⡙⠎⡶⢯⢏⡝⣰⣟⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣣⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡮⣻⣿⣿⠿⠿⠟⠐⠺⠿⣿⣿⠟⠵⠟⠉⠀⠀⠀⠀⠀⠀⠀⠎⢡⠔⠚⢀⠀⠀⠀⠀⠀⠀⠑⡘⣿⣿⠟⡓⠔⣠
# ⣷⣻⠭⢂⠱⡐⠌⠆⡙⢤⡙⡎⠎⣼⢫⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⣵⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⡁⢀⡀⠀⠀⠛⠓⠦⢄⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠈⠀⠀⠀⠀⠀⠀⢠⡈⠇⣈⣴⣾⣿
# ⣩⣎⠷⢉⡐⢨⠐⡡⢉⢦⡱⡭⣼⢏⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣻⡄⠀⠀⠀⠀⠀⠀⠀⠈⠉⠛⠶⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀⠀⢀⣤⠀⠀⠀⠀⠀⢡⢤⣿⣿⣿⣿
# ⣋⣌⠢⡁⢆⢂⠖⡡⠏⠊⣡⢠⡿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠃⢾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠳⢆⣀⠀⠀⠀⡴⣖⣁⣠⡄⠈⠀⠀⠀⠀⠀⠀⢰⣿⣿⣿⣿⣿
# ⢓⣬⢳⡜⠢⢉⠂⡅⢎⠱⠂⢸⣿⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀⢺⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⣇⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⢿⣦⡻⣿⣿⡏⢠⣀⠀⠀⠁⠀⠀⠀⣿⣿⣿⣿⣿⣻
# ⡟⢎⡣⢌⡐⢂⠈⢀⠠⠐⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢏⡴⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣿⣎⣿⣶⣄⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠻⡜⣿⣿⡟⠉⣻⠖⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿
# ⡞⡬⠓⣈⠐⠠⠈⠀⠀⢄⠒⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⡿⢁⣾⠁⣇⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⣿⣿⡼⣿⣿⣦⢧⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⡿⠇⠀⠀⠀⠀⠀⠀⣼⣿⣿⣿⣿⣿⣽
# ⠤⡁⠃⠄⠀⠀⠠⡀⠄⠈⠈⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣽⣉⠀⢸⡇⠀⣿⡌⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣿⣿⣷⣽⣿⣿⣾⣿⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀⠀⠀⠀⠀⣼⣿⣿⣿⣿⣿⣻⣿
# ⣤⣤⣁⠠⠘⡈⢅⠒⡄⢂⠐⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡷⡈⠆⡄⡿⡗⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢱⠏⣿⣿⣿⣿⣿⣿⣿⣿⣻⢧⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠶⢇⢿⣿⣿⣿⣿⣿⣾⣿
# ⡟⣿⣿⡀⠄⠃⡜⢠⠑⡌⠐⠈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣃⡀⠁⢓⣥⣦⡙⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠈⣴⢿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠈⠿⣿⣿⣿⣿⣾⣿
# ⠙⠢⡝⠽⡀⠌⠰⡁⢎⠰⣁⠂⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⢯⡗⣴⣿⣿⣿⣿⣷⣬⣛⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢣⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⣛⣩⣤⣶⣤⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢿⣿⣿⣿⣿
# ⢈⠡⠌⢂⠁⢂⠁⡘⢄⠣⡐⠄⠈⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⣼⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢇⣿⣿⣿⣿⣿⣿⣿⣿⣿⠛⢉⣴⣿⣿⣿⣿⣿⣿⣿⣿⣮⡆⠄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣿⣿⣿
# ⢀⠞⡜⢦⣊⢄⡂⠐⢨⠐⡡⢊⠸⣷⣦⣄⠈⠉⠙⠛⠿⣿⣿⠿⠛⠉⠉⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⠘⠻⢏⣛⣿⠿⠛⢛⠁⣴⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⢘⣻⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿
# ⡌⣏⠸⡑⢎⢦⡱⢈⠀⠱⣀⠣⡀⢿⣿⣿⣷⣤⣄⣀⠀⠀⠀⠀⠀⠀⠀⠈⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⢀⡰⣀⢆⣠⣄⣤⠢⡘⢧⡹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠁⣾⣿⣿⣿⣷⣤⡀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿
# ⡜⣦⢅⡐⢌⡲⣱⠃⠌⡐⠠⢃⠔⡘⣿⣿⣿⣿⣿⣿⣧⡀⠀⠀⠀⠀⠀⠀⠘⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢃⡼⣎⣷⣽⣾⣿⣿⣿⣿⣷⣦⡠⣙⠻⠿⣿⣿⣿⣿⠿⠛⢭⣁⣤⣼⡙⢿⣿⣿⣿⣿⣿⣿⣶⣦⣤⣀⠀⢀⣽⣿⣿⣿
# ⠘⣦⢫⣔⣣⢳⡅⡋⡔⡀⢂⠡⢊⠄⠹⣿⣿⣿⣿⣿⣿⣿⣶⣴⢢⠀⣀⠀⠀⠀⠙⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⣡⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣞⢿⣿⣶⣶⣶⣶⣶⣿⣿⣿⣿⣿⣿⣶⣝⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
# ⣙⠶⡣⠞⣌⠳⣌⠱⡄⠱⡀⠐⠠⠈⠀⢻⣿⣿⣿⣿⣿⣿⣿⣿⣾⢀⣿⣷⣤⣀⠀⠀⠀⠉⠛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢏⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣮⣛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
# ⣬⠳⣡⢋⡔⢣⠌⠑⠨⡁⠐⠀⢀⣀⣠⡘⣿⣿⣿⣿⣿⣿⣿⣿⡟⣼⣿⣿⣿⣿⣿⣶⣦⣤⣀⣀⡀⠉⠙⠻⠿⠿⠿⠟⠡⢾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
# ⡔⣫⠔⢪⠜⡡⠊⠐⣀⣴⣶⣿⣿⣿⣿⣿⣬⡛⢿⣿⣿⣿⣿⣿⢡⢺⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣤⣤⡤⠀⠀⠀⠠⢈⡉⠛⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
# ⡘⡄⠋⡄⠂⢀⣵⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣜⡿⣿⡟⢃⢺⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⠀⠀⠀⠐⠠⠀⡌⡑⢊⠖⢤⢩⡙⠛⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
# ⠱⡈⠅⢀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡳⠃⣰⣿⠻⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠋⠀⠀⠀⠀⡐⠠⢄⠂⡄⠑⡊⠜⡢⢆⠭⣙⠲⢆⠦⣉⢛⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
# ⡑⠌⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⠋⠁⢀⣠⣯⣶⣿⣿⣿⣿⣿⡿⣿⣿⣿⠿⠛⠋⠀⠀⠀⠠⠐⠠⢡⠐⡄⢂⠡⣈⠱⢈⠒⡌⠌⠓⢭⠲⣌⡑⠣⢍⠳⡌⠭⡙⠻⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
