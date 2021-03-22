import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotifyIDs
import csv
import datetime
import pandas as pd

#csv_file = csv.reader(open('spx_1950-2020.csv', "r"), delimiter=',')
csv_file = pd.read_csv('spx_1950-2020.csv')
dateColumn = csv_file.Date
closeColumn = csv_file.Close

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=spotifyIDs.clientID,
                                                           client_secret=spotifyIDs.clientSecret))

#results = sp.search(q='kanye', limit=10)
# for idx, album in enumerate(results['album']['items']):
#    print(idx, album['name'])


kanyeURI = 'spotify:artist:5K4W6rqBFWDnAN6FQUkS6x'
results = sp.artist_albums(kanyeURI, album_type='album')
albums = results['items']
while results['next']:
    results = sp.next(results)
    albums.extend(results['items'])

albumDict = dict()  # Stores album name / release date pairs
albumDatesSet = set()  # Stores unique release dates

for album in albums:
    # For all albums, need to check for duplicate names and duplicate dates
    if album['name'] not in albumDict and album['release_date'] not in albumDatesSet:
        albumDict[album['name']] = album['release_date']
        albumDatesSet.add(album['release_date'])

# print(albumDict)

forsight = 5

for count, row in enumerate(dateColumn):
    for releaseDate in albumDatesSet:
        if row == releaseDate:
            # Found release date. Need to get current value and compare against value x days after
            delta = closeColumn[count] - closeColumn[count+forsight]
            print(releaseDate, delta)
