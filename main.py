import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
# Constants
CLIENT_ID = "[YOUR_CLIENT_ID]"
CLIENT_SECRET = "[YOUR_CLIENT_SECRET]"


# Date from input
def get_date():
    return input("Which year do you want to listen? Type the date in this format YYYY-MM-DD:")


# Get Webpage
def get_web_page(url):
    response = requests.get(url=url)
    return response.text


# Create list of tracks from webpage
def get_name_of_songs(web_page):
    soup = BeautifulSoup(web_page, "html.parser")
    tracks = soup.select("li ul li h3")
    names_of_songs = [s.getText().strip() for s in tracks]
    return names_of_songs


# Create list of URI of tracks
def create_tracks_uri(sp, songs, year):
    new_playlist = []
    for song in songs:
        try:
            spotify_result = sp.search(q=f"track:{song} year:{year}", type="track")
            spotify_uri = spotify_result["tracks"]["items"][0]["uri"]
            new_playlist.append(spotify_uri)
        except IndexError:
            pass
    return new_playlist


# Main
def main():
    date = get_date()
    url = f"https://www.billboard.com/charts/hot-100/{date}/"
    # Year from date
    year = date.split("-")[0]

    web_page = get_web_page(url)

    songs = get_name_of_songs(web_page)

    #SPOTIFY
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                                   client_secret=CLIENT_SECRET,
                                                   redirect_uri="http://example.com",
                                                   scope="playlist-modify-private",
                                                   show_dialog=True,
                                                   cache_path="token.txt",
                                                   username="[YOUR_USERNAME]"))

    user_id = sp.current_user()["id"]

    # Create new playlist on Spotify
    my_playlist = sp.user_playlist_create(user=f"{user_id}", name=f"{year} Billboard Top Tracks", public=False,
                                          description=f"Top Tracks from {year}")

    # Add songs to playlist
    sp.playlist_add_items(playlist_id=my_playlist["id"], items=create_tracks_uri(sp, songs, year))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()


