import spotipy
import sys
from spotipy.oauth2 import SpotifyClientCredentials
import spotifyIDs
import csv
import datetime
import pandas as pd
import statistics
from colorama import init, Fore, Back, Style

init()  # Initialize colorama for Windows

#csv_file = csv.reader(open('spx_1950-2020.csv', "r"), delimiter=',')
csv_file = pd.read_csv('spx_1950-2020.csv')
dateColumn = csv_file.Date
closeColumn = csv_file.Close

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=spotifyIDs.clientID,
                                                           client_secret=spotifyIDs.clientSecret))

# Checks for input argument, default to Kanye if none
if len(sys.argv) > 1:
    name = ''.join(sys.argv[1:])
else:
    name = 'Kanye West'
# Search from input and get first result
resultsArtist = sp.search(q='artist:' + name, type='artist')
items = resultsArtist['artists']['items']

if len(items) > 0:
    artist = items[0]

print(artist['name'])

results = sp.artist_albums(artist['uri'], album_type='album')
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

# TODO make user programmable and/or search around the value
forsight = 5

deltaList = []

color = Fore.RED

# Reverse key/value pair allowing us to find album title by date
albumDatesTitle = [(a, b) for b, a in albumDict.items()]

for count, row in enumerate(dateColumn):
    for releaseDate in albumDatesSet:
        if row == releaseDate:
            # Found release date. Need to get current value and compare against value x days after
            delta = round(
                100 * (closeColumn[count+forsight] - closeColumn[count]) / closeColumn[count], 2)
            deltaList.append(delta)
            albumTitle = ''
            for date in albumDatesTitle:
                if date[0] == releaseDate:
                    albumTitle = date[1]
            print(releaseDate, albumTitle, '', end='')
            if delta > 0:
                color = Fore.GREEN
            else:
                color = Fore.RED
            print(color + '', delta, '%', sep='')
            print(Style.RESET_ALL, end='')

print()
averageDelta = round(sum(deltaList) / len(deltaList), 2)
standardDeviation = round(statistics.stdev(deltaList), 2)

if averageDelta > 0:
    color = Fore.GREEN
else:
    color = Fore.RED
print(color + '', averageDelta, '%', sep='', end='')
print(Style.RESET_ALL, end='')
print(' ,', standardDeviation)
