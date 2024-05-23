# Importing necessary libraries
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn

# Importing the recommendation function on the recommendation.py file
from recommendation import recommend_song, graphic_spectogram, update_times_played, get_lyrics

# Function to clean the artist and title of a song to make it more readable
def cleaned_data(artist:str, genre:str, title:str):
    artist = artist.replace("_"," ")
    title = title.replace(".mp3","").replace(artist,"").replace(genre,"").replace(".","").replace("_","").replace(",","").replace("-","").replace("(lyrics)","").replace("(Official Video)","").replace("(Official Music Video)","").replace("Official Video","").replace("[]","").replace("()","").replace("Music Video","").replace("(Lyrics)","").replace("(video)","").replace("(Video)","").replace("VIDEO","").replace(" ft ","")
    return [artist, title]


# Creating the FastAPI instance
app = FastAPI() 


# Create a route to serve the static files
app.mount("/static", StaticFiles(directory="Playlist"), name="static")
app.mount("/static3", StaticFiles(directory="Users"), name="static3")
app.mount("/static4", StaticFiles(directory="Home_Page2"), name="static4")

# Create the templates instance to use Jinja2
templates = Jinja2Templates(directory="Playlist")
templates2 = Jinja2Templates(directory="Home_Page2")



# Create the route for the status of the server and the hello world message
@app.get("/helloworld")
def greeting():
    return {"message": f"Hello World. Welcome to my first web app. Add /home to the URL to see the home page."}

@app.get("/status")
async def status():
    return {"status": "running"}


# Create the main route for user authentication
@app.get("/")
async def user():
    return FileResponse("Users/index.html")


# Create the route for the home page
@app.get("/home/music")
async def home(request: Request):
    return templates2.TemplateResponse(
        request=request, name="index.html", context={"title": "Side To Side.mp3", "artist": "artist", "genre": "POP", "title_show": "Duckify", "artist_show":"by Pato & Pepechui"}
    )

# Create the route for the home page with the song information
@app.get("/home/music/{genre}/{artist}/{title}")
async def musicHome(request: Request, genre: str, artist: str, title:str):
    artist_show = cleaned_data(artist, genre, title)[0]
    title_Show = cleaned_data(artist, genre, title)[1]
    update_times_played(f"/tracks/{genre}/{artist}/{title}")
    if True:
        return templates2.TemplateResponse(
        request=request, name="index.html", context={"title": title, "artist": artist, "genre": genre, "id": 1, "title_show":title_Show, "artist_show":artist_show}
    )
    return {"error":f"error in the path {genre}/{artist}/{title}"}


# Create the route for the recommendation of a song
@app.get("/home2/music/{genre}/{artist}/{title}", response_class=HTMLResponse)
async def get_next_song_home(request: Request, genre: str, artist: str, title:str):
    path = f"/tracks/{genre}/{artist}/{title}"
    if True:
        a = recommend_song(path,genre)
        genre = a["genre"]
        artist = a["artist"]
        title = a["title"]
        artist_show = cleaned_data(artist, genre, title)[0]
        title_Show = cleaned_data(artist, genre, title)[1]
        return templates2.TemplateResponse(
        request=request, name="index.html", context={"title": title, "artist": artist, "genre": genre, "title_show": title_Show, "artist_show":artist_show}
    )
    return {"error":f"error in the path {path}"}


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


# Main function to run the server
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=4444, timeout_keep_alive=120)

