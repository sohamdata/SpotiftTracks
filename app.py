import requests
import base64  # used to encode binary data to ASCII chars
import json
from secrets import clientSecret, clientID
authurl = "https://accounts.spotify.com/api/token"
headers = {}
data = {}


def getAccessToken(clientID, clientSecret):
    # encode clientID and clientSecret
    headers['Authorization'] = "Basic " + base64.b64encode(
        f"{clientID}:{clientSecret}".encode('ascii')).decode('ascii')
    data['grant_type'] = "client_credentials"
    res = requests.post(authurl, headers=headers, data=data)
    # print(res.json())
    accessToken = res.json()['access_token']
    return accessToken


def getPlaylistTracks(token, playlistID):
    playlistEndPoint = f"https://api.spotify.com/v1/playlists/{playlistID}"
    headers['Authorization'] = f"Bearer {token}"
    res = requests.get(playlistEndPoint, headers=headers)
    # print(res.json())
    playlistObject = res.json()
    return playlistObject


def __main__():

    token = getAccessToken(clientID, clientSecret)
    print("get tracks from spotify playlist")

    # https://open.spotify.com/playlist/3waDnb5oM1smACvgJwcxbA?si=cf691924bb174fc3&nd=1
    # playlistID = "3waDnb5oM1smACvgJwcxbA"
    playlistID = input("Enter playlist link: ").split("/")[-1].split("?")[0]
    playlist = getPlaylistTracks(token, playlistID)

    print(f"\n\n{playlist['name']}, by {playlist['owner']['display_name']}")
    print(f"tracks: {playlist['tracks']['total']}")
    for t in playlist['tracks']['items']:
        print('____________________________________________________')
        for a in t['track']['artists']:
            print(a['name'])
        songName = t['track']['name']
        print(songName)

    with open("playlist.json", "w") as f:
        json.dump(playlist, f, indent=4)


if __name__ == "__main__":
    __main__()
