# app/api/v1/router/router.py
# pylint: disable-all
# type: ignore
from fastapi import APIRouter

from api.v1.endpoints.user_interaction.user_interaction import router as user_interaction_router
from api.v1.endpoints.user_role.user_role import router as user_role_router
from api.v1.endpoints.user_role_association.user_roles_association import (
    router as user_role_association_router,
)
from api.v1.endpoints.users.users import router as users_router
from api.v1.endpoints.users_matching.users_matching import router as users_matching_router

api_router = APIRouter()
api_router.include_router(users_router, prefix="/api/v1", tags=["Users"])
api_router.include_router(user_role_router, prefix="/api/v1", tags=["User role"])
api_router.include_router(
    user_role_association_router, prefix="/api/v1", tags=["User role association"]
)
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
