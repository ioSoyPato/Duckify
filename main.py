# Load csvs
import pandas as pd
import re as r
import random


ROCK = pd.read_csv("DataBase/ROCK.csv")
ROCK["Genre"] = "ROCK" 
ROCK["id"] = ROCK["id"].str.replace("ROCK","")

ELECTRONIC = pd.read_csv("DataBase/ELECTRONIC.csv")
ELECTRONIC["Genre"] = "ELECTRONIC" 
ELECTRONIC["id"] = ELECTRONIC["id"].str.replace("ELECTRONIC","")

POP = pd.read_csv("DataBase/POP.csv")
POP["Genre"] = "POP" 
POP["id"] = POP["id"].str.replace("POP","")

RAP = pd.read_csv("DataBase/RAP.csv")
RAP["Genre"] = "RAP" 
RAP["id"] = RAP["id"].str.replace("RAP","")

# Concatenar todos los DataFrame
SONGS_DB = pd.concat([ROCK, ELECTRONIC, POP, RAP])

SONGS_DB.drop("Unnamed: 0", axis=1, inplace=True)
SONGS_DB.drop("id",axis=1,inplace=True)

SONGS_DB["ID"] = range(1,len(SONGS_DB)+1)

currented_played = []
def recommend_song(path:str, genre:str):
    currented_played.append(path)
    randipity = random.randint(0,6)
    if randipity >=3:
        current_genre = SONGS_DB[SONGS_DB["Genre"]==genre].head(1).Genre.unique()[0]
        recommendation = SONGS_DB[~SONGS_DB["shortedPath"].isin(currented_played)]
        recommendation = recommendation[recommendation["Genre"]== current_genre].head(1).shortedPath.unique()[0]
    else:
        current_genre = SONGS_DB[SONGS_DB["Genre"]!=genre].Genre.unique()[random.randint(0,2)]
        recommendation = SONGS_DB[~SONGS_DB["shortedPath"].isin(currented_played)]
        recommendation = recommendation[recommendation["Genre"]== current_genre].head(1).shortedPath.unique()[0]
    
    recommendation = recommendation.split("/")
    
    return {"genre":recommendation[2], "artist":recommendation[3], "title":recommendation[4]}

### CHAT ###


### FASTAPI ###

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


app = FastAPI()

# Create a route to serve the static files
app.mount("/static", StaticFiles(directory="Playlist"), name="static")
app.mount("/static2", StaticFiles(directory="Home_Page"), name="static2")
app.mount("/static3", StaticFiles(directory="Users"), name="static3")
app.mount("/static4", StaticFiles(directory="Home_Page2"), name="static4")

templates = Jinja2Templates(directory="Playlist")
templates2 = Jinja2Templates(directory="Home_Page2")

@app.get("/playlist/{genre}/{artist}/{title}", response_class=HTMLResponse)
async def read_item(request: Request, genre: str, artist: str, title: str):
    artist_show = artist.replace("_"," ")
    title_Show = title.replace(".mp3","").replace(artist_show,"").replace(genre,"").replace(".","").replace("_","").replace(",","").replace("-","").replace("(lyrics)","").replace("(Official Video)","").replace("(Official Music Video)","").replace("Official Video","").replace("[]","").replace("()","").replace("Music Video","").replace("(Lyrics)","")
    return templates.TemplateResponse(
        request=request, name="index.html", context={"title": title, "artist": artist, "genre": genre, "title_Show":title_Show}
    )

@app.get("/playlist2/{genre}/{artist}/{title}", response_class=HTMLResponse)
async def get_next_song(request: Request, genre: str, artist: str, title:str):
    path = f"/tracks/{genre}/{artist}/{title}"
    if True:
        a = recommend_song(path,genre)
        genre = a["genre"]
        artist = a["artist"]
        title = a["title"]
        artist_show = artist.replace("_"," ")
        title_Show = title.replace(".mp3","").replace(artist_show,"").replace(genre,"").replace(".","").replace("_","").replace(",","").replace("-","").replace("(lyrics)","").replace("(Official Video)","").replace("(Official Music Video)","").replace("Official Video","").replace("[]","").replace("()","").replace("Music Video","").replace("(Lyrics)","")
        return templates.TemplateResponse(
        request=request, name="index.html", context={"title": title, "artist": artist, "genre": genre, "id": id, "title_Show": title_Show}
    )
    return {"error":f"error in the path {path}"}

@app.get("/helloworld")
def greeting():
    return {"message": f"Hello World. Welcome to my first web app. Add /home to the URL to see the home page."}
    
@app.get("/home")
async def home():
    return FileResponse("Home_Page/index.html") 

@app.get("/home/music/{genre}/{artist}/{title}")
async def musicHome(request: Request, genre: str, artist: str, title:str):
    artist_show = artist.replace("_"," ")
    title_Show = title.replace(".mp3","").replace(artist_show,"").replace(genre,"").replace(".","").replace("_","").replace(",","").replace("-","").replace("(lyrics)","").replace("(Official Video)","").replace("(Official Music Video)","").replace("Official Video","").replace("[]","").replace("()","").replace("Music Video","").replace("(Lyrics)","")
    if True:
        return templates2.TemplateResponse(
        request=request, name="index.html", context={"title": title, "artist": artist, "genre": genre, "id": id, "title_show":title_Show, "artist_show":artist_show}
    )
    return {"error":f"error in the path {genre}/{artist}/{title}"}

@app.get("/")
async def user():
    return FileResponse("Users/index.html")

@app.get("/status")
async def status():
    return {"status": "running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=4444, timeout_keep_alive=120)
