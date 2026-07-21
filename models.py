from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship # importing column types 

from database import Base


class User(Base): # We are creating a user model because in a real application a  post should be associated with a actual user accounts, since we are going to setup authentication later on its better to set up good relationships now and will help us avoid complex database schemas later 
    __tablename__ = "users" # This tells sqlalchemy what the name of the table is 

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True) # id is the primary key and that makes auto increment possible
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False) # username is a required field due to nullable = False and should be unique for each entry
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    image_file: Mapped[str | None] = mapped_column(String(200),nullable=True,default=None,) # this can either be a str or none, this is going to store just the file names to the images like im.jpeg . this decouples or database from the file structure so we were to reorganize our files later and rename some directories then we dont need to update the database and just change or rename things. Separates the data from presentation 

    posts: Mapped[list[Post]] = relationship(back_populates="author") # This a one to many relationship, one user can have many posts adn back_populates here points to the author and that means it links to a author field on the post. This allows us to do user.posts later on to grab all of users post. Here the post is referenced earlier and defined later on in code below, this is something called as FORWARD REFERENCE and as currently i have the python version 3.12.3 we need to add the 1st line of the code to make this runnable but in python 3.14 this gets sorted out automatically  

    @property
    def image_path(self) -> str: # This is python related not db, this is for if an user has an uploaded custom image then we are going to return that image from the 1st return statement but if not then we return a static image from the 2nd return statement. This is a best practice generally 
        if self.image_file:
            return f"/media/profile_pics/{self.image_file}"
        return "/static/profile_pics/default.jpg"




class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"),nullable=False,index=True,) # Foreign key links the post to users, index=true to make sure posts have index as this is not a primary key so indexes are not auto incremented and since we are indexing posts here the writes in the database are slightly slower 
    date_posted: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), # timezone aware storage and will help when migrating to postgres later
        default=lambda: datetime.now(UTC),
    )

    author: Mapped[User] = relationship(back_populates="posts") # links back to user.post and helps us do post.author to get the user back
