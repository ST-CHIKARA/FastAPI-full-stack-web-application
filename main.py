# This project is from the corey schafer fastapi learning playlist

# Video - 1


from fastapi import FastAPI
app = FastAPI()





posts: list[dict] = [
    {
        "id": 1,
        "author": "Corey Schafer",
        "title": "FastAPI is Awesome",
        "content": "This framework is really easy to use and super fast.",
        "date_posted": "April 20, 2025",
    },
    {
        "id": 2,
        "author": "Jane Doe",
        "title": "Python is Great for Web Development",
        "content": "Python is a great language for web development, and FastAPI makes it even better.",
        "date_posted": "April 21, 2025",
    },
]




# @app.get("/") # use of decorator and "/" simply in the context of web dev that when i am trying to access a web page just the forward slash / after the domain for example www.google.com/ :- this slash to be put simply points towards the home page or in other context than the web dev denotes to root directory and if i want to access a about page the domain will look like www.google.com/about here /about is a path to about page and jointly these are called routes  
# def home():
#     return {"message": "Hello World"} 



@app.get("/api/posts")
def get_posts():
    return posts


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


templates = Jinja2Templates(directory="templates") # We created a template object that knows where our templates directory is 

# After writing the above step i commented out the previous routes that we wrote under video - 1

@app.get("/", include_in_schema=False, name="home")
@app.get("/posts", include_in_schema=False, name="posts")
def home(request: Request): # We will be adding a request parameter as a argument here because it is required by jinja2 (template engine)
    return templates.TemplateResponse(request, "home.html", {"posts": posts, "title": "Home"}, ) # The 3rd argument here is referred as a context dictionary and this dictionary contains all the variables that we wanna be able to use in our template.



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

@app.get("/api/posts/{post_id}") # post_id is what we are going to be capturing as a path parameter
def get_post(post_id: int): # here this type hint is important because fastapi uses it to validate the input
    for post in posts:
        if post.get("id") == post_id: # comparing the id of each dictionary with the path variable 
            return post
    #return {"error": "Post not found"} # here this is a basic way to handle the error will move forward on this topic later

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found") # after this the dev server will show the 404 status code 

# When we try to access a post that is not present as in case if i do localhost:8000/api/posts/5 the browser will show our error message but the server running in the terminal shows a 200 success status code which should be a 404 as the post was not find and to do that we have to raise a http exception with a proper 404 status code and this is a good restful api best practice. 

 
# for the web route


@app.get("/posts/{post_id}", include_in_schema=False) 
def post_page(request: Request, post_id: int): 
    for post in posts:
        if post.get("id") == post_id:
            title = post["title"][:50]
            return templates.TemplateResponse(request, "post.html", {"post": post, "title": title}, )   
            
    #return {"error": "Post not found"} # here this is a basic way to handle the error will move forward on this topic later

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found") 


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
