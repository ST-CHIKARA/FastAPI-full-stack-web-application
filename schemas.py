from pydantic import BaseModel, ConfigDict, Field # BaseModel is the base class that all our pydantic models inherit from, field lets us add constraints like min and max length, configdict helps us to configure models


class PostBase(BaseModel): # this func's info will be seen in docs
    title : str = Field(min_length=1, max_length=100)
    content : str = Field(min_length=1)
    author : str = Field(min_length=1, max_length=50)

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    model_config = ConfigDict(from_attributes=True) # In python version 2 we configure models with ConfigDict which was previously done with config class, so setting from_attributes=True tells pydantic to read data from attributes and not just dictionaries 

    # Since we currently have our data in dictionaries we access that through post["title"] but due to we configuring our model to take attributes and when we add a database we would be able to access the data through . notation post.title

    id : int # here using id is a standard convention to write a field rather than not writing it like this because its a python built in 
    date_posted : str # prior to adding a database it will be a string as in memory data use string for dates but when we add a database it will change to date time. 