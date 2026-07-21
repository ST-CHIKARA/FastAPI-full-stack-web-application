# This project is from the corey schafer fastapi learning playlist

# Video - 1


from fastapi import FastAPI
app = FastAPI()


# From video - 5

from typing import Annotated
from fastapi import Depends # For dependancy injections, its how we will inject the database sessions into out routes
from sqlalchemy import select
from sqlalchemy.orm import Session # for typehints
import models # models gives us access to our posts and user models we just created 
from database import Base, engine, get_db  # Base and engine are for creating tables, get_db is our dependancy function that provides our database sessions
from schemas import PostCreate, PostResponse, UserCreate, UserResponse
Base.metadata.create_all(bind=engine)

# Changes made in video - 5, since we connected a database in our 5th video we no longer need the posts data written below 

# posts: list[dict] = [
#     {
#         "id": 1,
#         "author": "Corey Schafer",
#         "title": "FastAPI is Awesome",
#         "content": "This framework is really easy to use and super fast.",
#         "date_posted": "April 20, 2025",
#     },
#     {
#         "id": 2,
#         "author": "Jane Doe",
#         "title": "Python is Great for Web Development",
#         "content": "Python is a great language for web development, and FastAPI makes it even better.",
#         "date_posted": "April 21, 2025",
#     },
# ]




# @app.get("/") # use of decorator and "/" simply in the context of web dev that when i am trying to access a web page just the forward slash / after the domain for example www.google.com/ :- this slash to be put simply points towards the home page or in other context than the web dev denotes to root directory and if i want to access a about page the domain will look like www.google.com/about here /about is a path to about page and jointly these are called routes  
# def home():
#     return {"message": "Hello World"} 



# This endpoint was modified due to certain changes that i learned in video - 4 adn this endpoint was copied and pasted on line 190 with further modifications

# @app.get("/api/posts")
# def get_posts():
#     return posts


from fastapi.responses import HTMLResponse

# @app.get("/", response_class=HTMLResponse, include_in_schema=False) # By doing include_in_schema=False we are saying dont include these in fastapi docs as these are html endpoints which are only used for humans to see and not used for programmable logic but this written logic here, this code will still work in the browser. 
# @app.get("/posts", response_class=HTMLResponse ,include_in_schema=False) # We can stack multiple decorators on the same function
# def home():
#     return f"<h1>{posts[0]["title"]}</h1>"



# Video - 2

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app.mount("/static", StaticFiles(directory="static"), name="static") # This mount method takes 3 arguments :- 1. the url path where the static files will be accessible, 2. static file instance that points to our static directory, 3. name we can use to reference in our templates  

# from video - 5

app.mount("/media", StaticFiles(directory="media"), name="media")

templates = Jinja2Templates(directory="templates") # We created a template object that knows where our templates directory is 

# After writing the above step i commented out the previous routes that we wrote under video - 1

# commented out and updated in video - 5

@app.get("/", include_in_schema=False, name="home")
@app.get("/posts", include_in_schema=False, name="posts")
def home(request: Request, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.Post))
    posts = result.scalars().all()
    return templates.TemplateResponse(
        request,
        "home.html",
        {"posts": posts, "title": "Home"},
    )

# @app.get("/", include_in_schema=False, name="home")
# @app.get("/posts", include_in_schema=False, name="posts")
# def home(request: Request): # We will be adding a request parameter as a argument here because it is required by jinja2 (template engine)
#     return templates.TemplateResponse(request, "home.html", {"posts": posts, "title": "Home"}, ) # The 3rd argument here is referred as a context dictionary and this dictionary contains all the variables that we wanna be able to use in our template.



# Video - 3

# In this video we will be learning about url parameters and how we can use those to get specific resources from our data.
# For example instead of returning all of our posts at once we can use path parameters to grab a single post instead. 

# We will be making both a api endpoint and a template page for viewing individual posts. We will also be making the posts homepage clickable and also learn about type validation with proper error handling


# Path parameters are a variable that are parts of the url path



from fastapi import HTTPException, status # For raising http exception and handling http status codes 

# these are to setup the error handling web routes 
from fastapi.exceptions import RequestValidationError # for handling validation errors
from fastapi.responses import JSONResponse # so that we can return json responses from our exception handler
from starlette.exceptions import HTTPException as starlettehttpexception # because fastapi is built on top of starlette and we are including the figurative root to handle the errors

# for the api route

# this api route was modified in video - 4, thats why this was commented out 

# @app.get("/api/posts/{post_id}") # post_id is what we are going to be capturing as a path parameter
# def get_post(post_id: int): # here this type hint is important because fastapi uses it to validate the input
    # for post in posts:
        # if post.get("id") == post_id: # comparing the id of each dictionary with the path variable 
            # return post
    #return {"error": "Post not found"} # here this is a basic way to handle the error will move forward on this topic later

    # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found") # after this the dev server will show the 404 status code 

# When we try to access a post that is not present as in case if i do localhost:8000/api/posts/5 the browser will show our error message but the server running in the terminal shows a 200 success status code which should be a 404 as the post was not find and to do that we have to raise a http exception with a proper 404 status code and this is a good restful api best practice. 

 
# for the web route

# commented and updated for video - 5

@app.get("/posts/{post_id}", include_in_schema=False)
def post_page(request: Request, post_id: int, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.Post).where(models.Post.id == post_id))
    post = result.scalars().first()
    if post:
        title = post.title[:50]
        return templates.TemplateResponse(
            request,
            "post.html",
            {"post": post, "title": title},
        )
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

# @app.get("/posts/{post_id}", include_in_schema=False) 
# def post_page(request: Request, post_id: int): 
#     for post in posts:
#         if post.get("id") == post_id:
#             title = post["title"][:50]
#             return templates.TemplateResponse(request, "post.html", {"post": post, "title": title}, )   
            
#     #return {"error": "Post not found"} # here this is a basic way to handle the error will move forward on this topic later

#     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found") 


# when we try to access a post that is not present we get a error message as a json that is good for the api endpoint but for a user seeing a frontend its not that good so we will handle it like this :- if the api endpoint is requested we will return the json error message but if its a web endpoint we will return a web api for that error message



# Error Handling

## StarletteHTTPException Handler
@app.exception_handler(starlettehttpexception)
def general_http_exception_handler(request: Request, exception: starlettehttpexception):
    message = (
        exception.detail
        if exception.detail
        else "An error occurred. Please check your request and try again."
    )

    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=exception.status_code,
            content={"detail": message},
        )
    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code": exception.status_code,
            "title": exception.status_code,
            "message": message,
        },
        status_code=exception.status_code,
    )


### RequestValidationError Handler
@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exception: RequestValidationError):
    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={"detail": exception.errors()},
        )
    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "title": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "message": "Invalid request. Please check your input and try again.",
        },
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
    )



# Video - 4

# Pydantic & Create schemas with request and response models
# Add field validation fo things like minimum and maximum length
# Update our get endpoint to use those response models 
# Create new post endpoint to add new post
# Testing in interactive docs


# What is Pydantic ?
# Its a data validation library that uses python type hints, it enforces them at runtime and give me detailed error responses. 

# We are covering this before adding the database because fastapi's biggest strength is how it integrates with pydantic. Schemas to find what data we accept from the clients and what data we returns and the database schemas defines what we store so we are keeping a separation of concerns here.

from schemas import PostCreate, PostResponse 

# from video - 5

# from video - 5 after updating the routes above 

# We need to add a template route for viewing a specific users post

## user_posts_page
@app.get("/users/{user_id}/posts", include_in_schema=False, name="user_posts")
def user_posts_page(
    request: Request,
    user_id: int,
    db: Annotated[Session, Depends(get_db)],
):
    result = db.execute(select(models.User).where(models.User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    result = db.execute(select(models.Post).where(models.Post.user_id == user_id))
    posts = result.scalars().all()
    return templates.TemplateResponse(
        request,
        "user_posts.html",
        {"posts": posts, "user": user, "title": f"{user.username}'s Posts"},
    )


@app.post(
    "/api/users",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)

def create_user(user: UserCreate, db:Annotated[Session,Depends(get_db)]): # dependancy injection what this means before running this function call get_db and pass the result as teh db parameter here 
    result = db.execute(select(models.User).where(models.User.username == user.username))
    existing_user = result.scalars().first() # gets first user object or None if there is no user match 

    if existing_user:
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,detail= "Username already exists",
        )
    

    result = db.execute(select(models.User).where(models.User.email == user.email))
    existing_email = result.scalars().first() # gets first user object or None if there is no user match 

    if existing_email:
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,detail= "Email already exists",
        )
    
    new_user = models.User(
        username = user.username,
        email = user.email,
    )

    db.add(new_user) # stages the insert
    db.commit() # commits to db
    db.refresh(new_user) # reloads the object from the db, although sqlalchemy autotracks the changes but this is a good practice 

    return new_user 


@app.get("/api/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db:Annotated[Session,Depends(get_db)]):
    result = db.execute(select(models.User).where(models.User.id == user_id))
    user = result.scalars().first()

    if user:
        return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

# New updated routes 

# 1. This endpoint is for us to get all posts by a user

@app.get("/api/users/{user_id}/posts", response_model=list[PostResponse])
def get_user_posts(user_id: int, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.User).where(models.User.id == user_id))
    user = result.scalars().first()
    if not user: # Checking if a user exist first, because if a empty list is returned when we are querying a user's post it can mean a user have no post or there is no user so we check for a user here 
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    result = db.execute(select(models.Post).where(models.Post.user_id == user_id))
    posts = result.scalars().all()
    return posts




# @app.get("/api/posts", response_model=list[PostResponse])
# def get_posts():
#     return posts

# Updated version below 

## get_posts
@app.get("/api/posts", response_model=list[PostResponse])
def get_posts(db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.Post))
    posts = result.scalars().all()
    return posts



# Create post endpoint

# commented out in video -5 after internal error
# @app.post(
#     "/api/posts",
#     response_model=PostResponse,
#     status_code=status.HTTP_201_CREATED,
# )

# commented out and updated after the commented code for video - 5

# def create_post(post: PostCreate):
#     new_id = max(p["id"] for p in posts) + 1 if posts else 1
#     new_post = {
#         "id": new_id,
#         "author": post.author,
#         "title": post.title,
#         "content": post.content,
#         "date_posted": "April 23, 2025",
#     }
#     posts.append(new_post)
#     return new_post


## create_post
@app.post(
    "/api/posts",
    response_model=PostResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_post(post: PostCreate, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.User).where(models.User.id == post.user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    new_post = models.Post(
        title=post.title,
        content=post.content,
        user_id=post.user_id,
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

# commented out and updated after the commented code 

# @app.get("/api/posts/{post_id}", response_model=PostResponse) # here we are returning just a single post not a list of posts so we expect a post response from a single post at this get endpoint
# def get_post(post_id: int): # here this type hint is important because fastapi uses it to validate the input
#     for post in posts:
#         if post.get("id") == post_id: # comparing the id of each dictionary with the path variable 
#             return post

#     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found") # after this the dev server will show the 404 status code 



## get_post
@app.get("/api/posts/{post_id}", response_model=PostResponse)
def get_post(post_id: int, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.Post).where(models.Post.id == post_id))
    post = result.scalars().first()
    if post:
        return post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")


# when we create a new post we get to see it on the homepage but as soon as we restart our server the post cant be seen again because we are storing the new post or posts currently in a list in temporary python memory. This problem will be solved in the next video that covers integrating a database in our project 
