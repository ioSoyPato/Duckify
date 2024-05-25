import pandas as pd
import os
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import librosa
import random
import numpy as np
import warnings
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from minisom import MiniSom

warnings.filterwarnings("ignore")

def creatingDF(genre):
    """
    Recieves a genre and returns a dataframe with all the songs of that genre
    """
    print(f"Creating {genre} df....")
    df = pd.DataFrame(columns=["id","artist", "song","spectogram","shortedPath"])
    for artist in [artist for artist in os.listdir(os.getcwd()+f"/tracks/{genre}") if artist != ".DS_Store"]:
        for song in [song for song in os.listdir(os.getcwd()+f"/tracks/{genre}/{artist}") if song != ".DS_Store"]:
            try:
                path = os.getcwd()+f"/tracks/{genre}/{artist}/{song}"
                shortedPath = f"/tracks/{genre}/{artist}/{song}"
                audio, sr = librosa.load(path, sr=None)
                duration = librosa.get_duration(y=audio, sr=sr)
    
                if duration > 60:
                    #Get a sample of 60 seconds of the song
                    start = random.randint(0, int(duration) - 60)
                    end = start + 60

                    audio = audio[int(start*sr):int(end*sr)]
                    D = librosa.amplitude_to_db(abs(librosa.stft(audio))) #Spectogram
                    D = D[:1025, :5168]

                    df.loc[len(df)] = [f'{genre}{len(df)+1}', artist, song, D, shortedPath]
            except:
                pass
    
    return df


def clustering(df):

    X = (df["spectogram"]).values.reshape(-1,)

    X_vector = np.array(list(map(lambda x: x.flatten(), X)))

    X_vector = X_vector.reshape(len(df), 1025 * 5168)


    pca = PCA(n_components=40)
    X_pca = pca.fit_transform(X_vector)

    kmeans = KMeans(n_clusters=5)
    kmeans.fit(X_pca)

    df['subgenres'] = kmeans.labels_
    df = df.loc[:, ['id', 'shortedPath', 'subgenres']]

    return df

def creatingSubGeneres(genre):
    clustering(creatingDF(genre)).to_csv(f"genres/{genre}.csv")

if __name__ == "__main__":
    
    for genre in [genre for genre in os.listdir(os.getcwd()+f"/tracks/") if genre != ".DS_Store"]:
        creatingSubGeneres(genre)

