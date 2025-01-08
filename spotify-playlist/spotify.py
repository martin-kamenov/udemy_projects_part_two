from bs4 import BeautifulSoup
from spotipy.oauth2 import SpotifyOAuth
import requests
import spotipy
import os

CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = "http://example.com"
chosen_date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
URL = f"https://www.billboard.com/charts/hot-100/{chosen_date}"
header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0"}
scope = "playlist-modify-private"

response = requests.get(url=URL, headers=header)
response.raise_for_status()
website_html = response.text

soup = BeautifulSoup(website_html, "html.parser")
all_songs = soup.select("li ul li h3")
songs = [song.getText().strip() for song in all_songs]

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope=scope,
        redirect_uri=REDIRECT_URI,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt",
    )
)
user = sp.current_user()
user_id = user["id"]
song_uris = []
year = chosen_date.split("-")[0]

for song in songs:
    result = sp.search(q=f"track:{song} year:{year}", type="track")

    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(user=user_id, name=f"{chosen_date} Billboard 100", public=False)
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)