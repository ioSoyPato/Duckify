# Importing necessary libraries
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Form, HTTPException, status
from fastapi.responses import RedirectResponse
import uvicorn
import pandas as pd
from fastapi import logger

# Importing the recommendation function on the recommendation.py file
from recommendation import recommend_song, graphic_spectogram, update_times_played, get_lyrics
from database_management import read_table_as_dataframe

# Function to clean the artist and title of a song to make it more readable
def cleaned_data(artist:str, genre:str, title:str):
    '''
    Input.
    artist: str, artist of the song
    genre: str, genre of the song
    title: str, title of the song

    Output.
    list, with the artist and title of the song cleaned

    Description.
    Clean the artist and title of a song to make it more readable using replace method (Needs to be improved with a regex method)
    '''
    artist = artist.replace("_"," ")
    title = title.replace(".mp3","").replace(artist,"").replace(genre,"").replace(".","").replace("_","").replace(",","").replace("-","").replace("(lyrics)","").replace("(Official Video)","").replace("(Official Music Video)","").replace("Official Video","").replace("[]","").replace("()","").replace("Music Video","").replace("(Lyrics)","").replace("(video)","").replace("(Video)","").replace("VIDEO","").replace(" ft ","")
    return [artist, title]


# Creating the FastAPI instance
app = FastAPI() 


# Create a route to serve the static files
app.mount("/static", StaticFiles(directory="Playlist"), name="static")
app.mount("/static3", StaticFiles(directory="Users"), name="static3")
app.mount("/static4", StaticFiles(directory="Home_Page2"), name="static4")
app.mount("/static5", StaticFiles(directory="Search"), name="static5")

# Create the templates instance to use Jinja2
templates = Jinja2Templates(directory="Playlist")
templates2 = Jinja2Templates(directory="Home_Page2")
templates3 = Jinja2Templates(directory="Search")


# immport credencials from the database (Beta)
credencial = read_table_as_dataframe("USER")

logger.logger.info("APP MOUNTED")

# Create the route for the status of the server and the hello world message
@app.get("/helloworld")
def greeting():
    logger.logger.info("SERVING ENDPOINT")
    return {"message": f"Hello World. Welcome to my first web app. Add /home to the URL to see the home page."}

@app.get("/status")
async def status():
    return {"status": "running"}

valid_user = False

# Create the main route for user authentication
@app.get("/")
async def user():
    return FileResponse("Users/index.html")


User = read_table_as_dataframe("USER")
SONG_DB = pd.read_csv("DataBase/SONGS_DB.csv")

# Create the user authentication route
@app.post("/login")
async def login(email: str = Form(...), password: str = Form(...), remember_me: bool = Form(False)):
    global valid_user
    if email in User["email"].to_list() and password in User.loc[User["email"]==email]["password"].to_list():
        # Redirect to home if login is successful
        valid_user = True
        response = RedirectResponse(url="/home/music", status_code=302)
        if remember_me:
            response.set_cookie(key="session", value="example_session_token", max_age=1800)  # 30 min
        return response
    else:
        raise HTTPException(status_code=400, detail="Invalid credentials")


# Create the route for the home page
@app.get("/home/music")
async def home(request: Request):
    if valid_user:
        return templates2.TemplateResponse(
            request=request, name="index.html", context={"title": "Side To Side.mp3", "artist": "artist", "genre": "POP", "title_show": "Duckify", "artist_show":"by Pato, Pepechui & Dafne"}
        )
    else:
        return RedirectResponse(url="http://127.0.0.1:4444/")

# Create the route for the home page with the song information
@app.get("/home/music/{genre}/{artist}/{title}")
async def musicHome(request: Request, genre: str, artist: str, title:str):
    artist_show = cleaned_data(artist, genre, title)[0]
    title_Show = cleaned_data(artist, genre, title)[1]
    update_times_played(f"/tracks/{genre}/{artist}/{title}")
    if valid_user:
        return templates2.TemplateResponse(
        request=request, name="index.html", context={"title": title, "artist": artist, "genre": genre, "id": 1, "title_show":title_Show, "artist_show":artist_show}
    )
    return RedirectResponse(url="http://127.0.0.1:4444/")


# Create the route for the recommendation of a song
@app.get("/home2/music/{genre}/{artist}/{title}", response_class=HTMLResponse)
async def get_next_song_home(request: Request, genre: str, artist: str, title:str):
    path = f"/tracks/{genre}/{artist}/{title}"
    if valid_user:
        a = recommend_song(path,genre)
        genre = a["genre"]
        artist = a["artist"]
        title = a["title"]
        artist_show = cleaned_data(artist, genre, title)[0]
        title_Show = cleaned_data(artist, genre, title)[1]
        return templates2.TemplateResponse(
        request=request, name="index.html", context={"title": title, "artist": artist, "genre": genre, "title_show": title_Show, "artist_show":artist_show}
    )
    return RedirectResponse(url="http://127.0.0.1:4444/")


# Create the method for the Lyric page
@app.get("/playlist/{genre}/{artist}/{title}", response_class=HTMLResponse)
async def read_item(request: Request, genre: str, artist: str, title: str):
    artist_show = cleaned_data(artist, genre, title)[0]
    title_Show = cleaned_data(artist, genre, title)[1]
    lyrics = get_lyrics(title_Show, artist_show)
    return templates.TemplateResponse(
        request=request, name="index.html", context={"title": title, "artist": artist, "genre": genre, "title_Show":title_Show,"lyrics":lyrics}
    )

# Create the route for the recommendation of a song with the Lyric page
@app.get("/playlist2/{genre}/{artist}/{title}", response_class=HTMLResponse)
async def get_next_song(request: Request, genre: str, artist: str, title:str):
    path = f"/tracks/{genre}/{artist}/{title}"
    if True:
        a = recommend_song(path,genre)
        genre = a["genre"]
        artist = a["artist"]
        title = a["title"]
        artist_show = cleaned_data(artist, genre, title)[0]
        title_Show = cleaned_data(artist, genre)[1]
        return templates.TemplateResponse(
        request=request, name="index.html", context={"title": title, "artist": artist, "genre": genre, "id": id, "title_Show": title_Show}
    )
    return {"error":f"error in the path {path}"}


# Create the like route (Beta)

# Create the rullete for all the songs
@app.get("/allmusic", response_class=HTMLResponse)
async def music_carousel(request: Request):
    SONGS_DB = pd.read_csv("DataBase/SONGS_DB.csv")
    songs = [
        {
            "url": f"http://127.0.0.1:4444/home/music/{row['Genre']}/{row['shortedPath'].split('/')[-1]}",
            "cover": "/static4/playlist-cover-1.png",  
            "title": row['shortedPath'].split('/')[-1].split('.')[0] 
        } for index, row in SONGS_DB.iterrows()
    ]
    # images =  get_images()
    images = ""
    return templates3.TemplateResponse("index.html", {"request": request, "songs": songs, "images": images,"title":"All Music","genre":"pop","artist":"Hola"})


# Main function to run the server
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=4444, timeout_keep_alive=120)

