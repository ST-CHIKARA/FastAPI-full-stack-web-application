from datetime import datetime
from pydantic import EmailStr

from pydantic import BaseModel, ConfigDict, Field # BaseModel is the base class that all our pydantic models inherit from, field lets us add constraints like min and max length, configdict helps us to configure models


class UserBase(BaseModel):
    username: str = Field(min_length=1, max_length=50)
    email: EmailStr = Field(max_length=120) # This EmailStr from pydantic validates that its a proper email format automatically so we dont need to write our own validation adn we dont need a min_length because EmailStr validated itself if its empty

class UserCreate(UserBase):
    pass

# One thing to note since our UserResponse inherits from UserBase, Our UserResponse is going to include the email field in the response, thats okay for now but returning a user's email in a public api response is a privacy concern and this will be fixed later by separating public and private schemas
#  
class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True) # so that pydantic can read from our sqlalchemy model

    id: int
    image_file: str | None
    image_path: str # This is a property on our user model

class PostBase(BaseModel): # this func's info will be seen in docs
    title : str = Field(min_length=1, max_length=100)
    content : str = Field(min_length=1)
    # author : str = Field(min_length=1, max_length=50) # was commented out due to it coming now from the User and Post relationship instead each post storing the author as plain text as in our dummy data  

class PostCreate(PostBase):
    user_id: int # temporary for testing, because when we create a post we are going to pass in user_id manually for now but when we add authentication we are going to get the current user from the session instead and that will be automatically be used there. 

class PostResponse(PostBase):
    model_config = ConfigDict(from_attributes=True) # In python version 2 we configure models with ConfigDict which was previously done with config class, so setting from_attributes=True tells pydantic to read data from attributes and not just dictionaries 

    # Since we currently have our data in dictionaries we access that through post["title"] but due to we configuring our model to take attributes and when we add a database we would be able to access the data through . notation post.title

    id : int # here using id is a standard convention to write a field rather than not writing it like this because its a python built in 
    #date_posted : str # prior to adding a database it will be a string as in memory data use string for dates but when we add a database it will change to date time. 
    user_id: int
    # date_posted type will become datetime instead of str
    date_posted: datetime
    author: UserResponse
    # When sqlalchemy loads a post it can also load the related user. Pydantic sees that author field, validates that user object against UserResponse and includes the ful user data in our api response. So we get nested JSON with the author, username, email, image_path automatically
