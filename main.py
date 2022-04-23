import requests
from bs4 import BeautifulSoup
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy


# create a spotify top 100 playlist on a specific date in past
billboard_endpoint = "https://www.billboard.com/charts/hot-100/"
date = input("What day do you want to travel to (input in the format YYYY-MM-DD e.g. 2012-07-15):")
billboard_endpoint += date
top_100 = requests.get(url=billboard_endpoint)
soup = BeautifulSoup(top_100.text, features="html.parser")
author_tags = soup.select("li>ul>li>span")
authors = []
counter = 0
for i in range(len(author_tags)):
    if i == 0:
        counter -= 1
        authors.append(author_tags[i].getText().strip())
    counter += 1
    if counter == 7:
        counter = 0
        authors.append(author_tags[i].getText().strip())
print(authors)

song_tags = soup.select("li h3#title-of-a-story")
songs = []
for song in song_tags:
    songs.append(song.getText().strip())
print(songs)

song_uris = []
scope = "playlist-modify-private"
sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

for song in songs:
    result = sp.search(q=f"track:{song}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
user_id = sp.current_user()["id"]
playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
print(song_uris)
