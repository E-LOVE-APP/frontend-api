from sqlalchemy import Column, String
from sqlalchemy.orm import validates
from base import BaseModel


class UserPost(BaseModel):
    __tablename__ = "user_post"

    post_title = Column(String(250), nullable=False)
    post_descr = Column(String(1000), nullable=False)
    # add category_id (many categories could be here)
    # add user_id here (1 user)
