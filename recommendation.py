# Import necessary libraries
import pandas as pd
import re as r
import random
import librosa
import matplotlib.pyplot as plt
import requests

from database_management import read_table_as_dataframe

# Read the csv (DataBase songs)
SONGS_DB = pd.read_csv("DataBase/SONGS_DB.csv")
SONGS_DB.set_index("ID", inplace=True)

# Drop all Unnameds
Unnamed = [0,0.1,0.2,0.3]

try:
    for i in Unnamed:
        SONGS_DB.drop(f"Unnamed: {i}",axis=1, inplace=True)
except:
    print("Already clean")

# Current played song variable creation
currented_played = []

# Function to update the times played of a song
def update_times_played(path:str):
    '''
    Input.
    path: str, path of the song to update the times played

    Output.
    None

    Description.
    Update the times played of a song in the DataBase
    '''
    SONGS_DB.loc[SONGS_DB["shortedPath"]==path, "TimesPlayed_Global"] += 1
    SONGS_DB.to_csv("DataBase/SONGS_DB.csv")
    print(f"Updated: {path}")

# Function to graph the song spectogram in comparison to the recommended song spectogram
def graphic_spectogram(path1:str, path2:str):
    '''
    Input.
    path1: str, path of the first song to compare
    path2: str, path of the second song to compare

    Output.
    dict, with the title of the songs

    Description.
    Create a spectogram of the songs and save it as a png
    '''
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

# Function to create a simple recommendation based on the SubGenre(spectrogram clustering) and the times played globally
def recommend_song(path:str, genre:str):
    '''
    Input.
    path: str, path of the song to recommend
    genre: str, genre of the song to recommend

    Output.
    dict, with the genre, artist and title of the recommended song

    Description.
    Create a simple recommendation based on the SubGenre(spectrogram clustering) and the times played globally of the songs
    '''
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

# Function to create a complex recommendation using a SARSA algorithm to recommend a song (R: Reward, Q: Quality)
def recommend_song_SARSA():
    pass

# Function to extract the lyrics of a song using requests 
def get_lyrics(title, artist):
    '''
    Input.
    title: str, title of the song
    artist: str, artist of the song

    Output.
    str, lyrics of the song

    Description.
    Extract the lyrics of a song using requests and a public API
    '''
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