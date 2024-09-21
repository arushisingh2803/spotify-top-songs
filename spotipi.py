from requests import post # to send request for access token
from requests import get # to request artist specific data
import json # data loaded in json
import os
import base64 # to encode authorisation string
from dotenv import load_dotenv # to import file with api keys!

load_dotenv() # this is to load in our environment variables(api keys!)

# importing client id from env file
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

# getting access token to request data
def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_token(token):
    return {"Authorization" : "Bearer " + token}

def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_token(token)
    query = f"?q={artist_name}&type=artist&limit=1"

    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]
    if len(json_result) == 0:
        return None
    return json_result[0]

def get_songs_by_artists(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=IE"
    headers = get_auth_token(token)
    result = get(url, headers=headers)  
    json_result = json.loads(result.content)["tracks"]
    return json_result

def input_artist():
    artistName = str(input("Enter name of artist: "))
    return artistName

token = get_token()
result = search_for_artist(token, input_artist())
artist_id = result["id"]
songs = get_songs_by_artists(token, artist_id)

for idx, song in enumerate(songs, start=1):
    print(f"{idx}. {song['name']}")
