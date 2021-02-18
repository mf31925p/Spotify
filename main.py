import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

CLIENT_ID = ""
CLIENT_SECRET = ""

date = input(" Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
year = date.split("-")[0]
print(year)
response = requests.get(f"https://www.billboard.com/charts/hot-100/{date}")
songs = response.text
soup = BeautifulSoup(songs, "html.parser")

song_titles = soup.find_all("span", class_="chart-element__information__song")
song_names = [song.getText() for song in song_titles]

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private playlist-read-private user-read-recently-played",
        redirect_uri="http://example.com",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)

user_id = sp.current_user()["id"]

song_uris = []

for song in song_names:
    results = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = results["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(user=user_id, name=f"Top 100 Songs {date}", public=False)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
