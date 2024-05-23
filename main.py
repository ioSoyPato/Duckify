# Load csvs
import pandas as pd
import re as r
import random
import librosa
import matplotlib.pyplot as plt

SONGS_DB = pd.read_csv("DataBase/SONGS_DB.csv")
SONGS_DB.set_index("ID", inplace=True)

# Drop all Unnameds
Unnamed = [0,0.1,0.2,0.3]

try:
    for i in Unnamed:
        SONGS_DB.drop(f"Unnamed: {i}",axis=1, inplace=True)
except:
    print("Already clean")
    
currented_played = []
def update_times_played(path:str):
    SONGS_DB.loc[SONGS_DB["shortedPath"]==path, "TimesPlayed_Global"] += 1
    SONGS_DB.to_csv("DataBase/SONGS_DB.csv")
    print(f"Updated: {path}")

def graphic_spectogram(path1:str, path2:str):
    path1 = f"Playlist/{path1}"
    title1 = r.split("/",path1)[-1]
    path2 = f"Playlist/{path2}"
    title2 = r.split("/",path2)[-1]
    audio, sr = librosa.load(path1, sr=None)
    D1 = librosa.amplitude_to_db(abs(librosa.stft(audio))) #Spectogram
    audio, sr = librosa.load(path2, sr=None)
    D2 = librosa.amplitude_to_db(abs(librosa.stft(audio))) #Spectogram

    # Graphic both spectograms
    fig, ax = plt.subplots(1, 2, figsize=(20, 5))
    ax[0].imshow(D1, aspect='auto', origin='lower')
    ax[0].set_title(title1)
    ax[0].set_xlabel("Time")
    ax[0].set_ylabel("Frequency")
    ax[1].imshow(D2, aspect='auto', origin='lower')
    ax[1].set_title(title2)
    ax[1].set_xlabel("Time")
    ax[1].set_ylabel("Frequency")
    
    # Save the figure as a png
    plt.savefig("Home_Page2/spects/spectograms.png")

    return {"title1":title1, "title2":title2}

# def recommend_song(path:str, genre:str):
#     currented_played.append(path)
#     randipity = random.randint(0,6)
#     if randipity >=3:
#         current_genre = SONGS_DB[SONGS_DB["Genre"]==genre].head(1).Genre.unique()[0]
#         recommendation = SONGS_DB[~SONGS_DB["shortedPath"].isin(currented_played)]
#         recommendation = recommendation[recommendation["Genre"]== current_genre].head(1).shortedPath.unique()[0]
#     else:
#         current_genre = SONGS_DB[SONGS_DB["Genre"]!=genre].Genre.unique()[random.randint(0,2)]
#         recommendation = SONGS_DB[~SONGS_DB["shortedPath"].isin(currented_played)]
#         recommendation = recommendation[recommendation["Genre"]== current_genre].head(1).shortedPath.unique()[0]
    
#     recommendation = recommendation.split("/")
    
#     return {"genre":recommendation[2], "artist":recommendation[3], "title":recommendation[4]}

def recommend_song(path:str, genre:str):
    currented_played.append(path)
    randipity = random.randint(0,6)
    update_times_played(path)
    if randipity >=3:
        current_genre = SONGS_DB[SONGS_DB["Genre"]==genre].head(1).Genre.unique()[0]
        recommendation = SONGS_DB[~SONGS_DB["shortedPath"].isin(currented_played)]
        recommendation = recommendation[recommendation["Genre"]== current_genre].sort_values("TimesPlayed_Global",ascending=False).head(1).shortedPath.unique()[0]
    else:
        current_genre = SONGS_DB[SONGS_DB["Genre"]!=genre].Genre.unique()[random.randint(0,2)]
        recommendation = SONGS_DB[~SONGS_DB["shortedPath"].isin(currented_played)]
        recommendation = recommendation[recommendation["Genre"]== current_genre].sort_values("TimesPlayed_Global",ascending=False).head(1).shortedPath.unique()[0]
    
    currented_played.append(recommendation)
    update_times_played(recommendation)
    # print(f"User History: {currented_played}") # Todays user history
    # print(graphic_spectogram(path,recommendation))
    recommendation = recommendation.split("/")
    
    return {"genre":recommendation[2], "artist":recommendation[3], "title":recommendation[4]}

def recommend_song_SARSA():
    pass

def get_lyrics(title, artist):
    import requests
    url = f"https://api.lyrics.ovh/v1/{artist}/{title}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if 'lyrics' in data:
            return data['lyrics']
        else:
            return "Lyrics not available. Sorry!"
    else:
        return "Lyrics not available. Sorry! 🐣🐣"

    

### CHAT Removed Feature###


### FASTAPI ###

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


def cleaned_data(artist:str, genre:str, title:str):
    artist = artist.replace("_"," ")
    title = title.replace(".mp3","").replace(artist,"").replace(genre,"").replace(".","").replace("_","").replace(",","").replace("-","").replace("(lyrics)","").replace("(Official Video)","").replace("(Official Music Video)","").replace("Official Video","").replace("[]","").replace("()","").replace("Music Video","").replace("(Lyrics)","").replace("(video)","").replace("(Video)","").replace("VIDEO","").replace(" ft ","")
    return [artist, title]


app = FastAPI()

# Create a route to serve the static files
app.mount("/static", StaticFiles(directory="Playlist"), name="static")
app.mount("/static3", StaticFiles(directory="Users"), name="static3")
app.mount("/static4", StaticFiles(directory="Home_Page2"), name="static4")

templates = Jinja2Templates(directory="Playlist")
templates2 = Jinja2Templates(directory="Home_Page2")

@app.get("/playlist/{genre}/{artist}/{title}", response_class=HTMLResponse)
async def read_item(request: Request, genre: str, artist: str, title: str):
    artist_show = cleaned_data(artist, genre, title)[0]
    title_Show = cleaned_data(artist, genre, title)[1]
    lyrics = get_lyrics(title_Show, artist_show)
    return templates.TemplateResponse(
        request=request, name="index.html", context={"title": title, "artist": artist, "genre": genre, "title_Show":title_Show,"lyrics":lyrics}
    )

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

@app.get("/helloworld")
def greeting():
    return {"message": f"Hello World. Welcome to my first web app. Add /home to the URL to see the home page."}
    
@app.get("/home")
async def home():
    return {"error":"This method doesnt exist anymore, please use /home/music"}

@app.get("/home/music/{genre}/{artist}/{title}")
async def musicHome(request: Request, genre: str, artist: str, title:str):
    artist_show = cleaned_data(artist, genre, title)[0]
    title_Show = cleaned_data(artist, genre, title)[1]
    update_times_played(f"/tracks/{genre}/{artist}/{title}")
    if True:
        return templates2.TemplateResponse(
        request=request, name="index.html", context={"title": title, "artist": artist, "genre": genre, "id": id, "title_show":title_Show, "artist_show":artist_show}
    )
    return {"error":f"error in the path {genre}/{artist}/{title}"}

@app.get("/home/music/{genre}/{artist}/{title}")
async def musicHome(request: Request, genre: str, artist: str, title:str):
    artist_show = cleaned_data(artist, genre, title)[0]
    title_Show = cleaned_data(artist, genre, title)[1]
    if True:
        return templates2.TemplateResponse(
        request=request, name="index.html", context={"title": title, "artist": artist, "genre": genre, "id": id, "title_show":title_Show, "artist_show":artist_show}
    )
    return {"error":f"error in the path {genre}/{artist}/{title}"}
    

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

@app.get("/home/music")
async def home(request: Request):
    return templates2.TemplateResponse(
        request=request, name="index.html", context={"title": "Side To Side.mp3", "artist": "artist", "genre": "POP", "title_show": "Duckify", "artist_show":"by Pato & Pepechui"}
    )

@app.get("/home/musci/like/{genre}/{artist}/{title}")
async def musicHome(request: Request, genre: str, artist: str, title:str):
    artist_show = cleaned_data(artist, genre, title)[0]
    title_Show = cleaned_data(artist, genre, title)[1]
    SONGS_DB.loc[SONGS_DB["shortedPath"]==f"/tracks/{genre}/{artist}/{title}", "liked"] = 1
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
    # Add classes and connect to an external database
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=4444, timeout_keep_alive=120)
