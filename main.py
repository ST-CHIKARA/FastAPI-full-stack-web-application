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

@app.get("/", response_class=HTMLResponse, include_in_schema=False) # By doing include_in_schema=False we are saying dont include these in fastapi docs as these are html endpoints which are only used for humans to see and not used for programmable logic but this written logic here, this code will still work in the browser. 
@app.get("/posts", response_class=HTMLResponse ,include_in_schema=False) # We can stack multiple decorators on the same function
def home():
    return f"<h1>{posts[0]["title"]}</h1>"




