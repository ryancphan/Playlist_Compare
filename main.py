import pandas as pd
import csv
import numpy
import copy
import os
from export_spotify_playlists import spotify_exporter
from itunes_library_to_csv import generate_csv

spotify_exporter.main()
generate_csv.main()
itunes_list = os.listdir("./itunes_playlists")
itunes_list = [os.path.splitext(x)[0] for x in itunes_list]
spotify_list = os.listdir("./spotify_playlists")
spotify_list = [os.path.splitext(x)[0] for x in spotify_list]

for spotify_playlist in spotify_list:
    print("spotify playlist : " + spotify_playlist)
    itunes_playlist = spotify_playlist
    if itunes_playlist in itunes_list:
        spotify_csv = pd.read_csv('spotify_playlists/' + spotify_playlist + '.csv')
        spotify_song_temp = spotify_csv['name'].tolist()
        spotify_song = []
        for song in spotify_song_temp:
            if ' - ' in song:
                spotify_song.append(song.replace('- ','(') +')')
            else:
                spotify_song.append(song)

        spotify_artist = spotify_csv['artist'].tolist()

        itunes_csv = pd.read_csv('itunes_playlists/' + itunes_playlist + '.csv', header=None)
        song_matrix = itunes_csv[itunes_csv.columns[0]].to_numpy()
        itunes_song = song_matrix.tolist()
        artist_matrix = itunes_csv[itunes_csv.columns[1]].to_numpy()
        itunes_artist = artist_matrix.tolist()

        spotify_dict = dict(zip(spotify_song, spotify_artist))
        itunes_dict = dict(zip(itunes_song, itunes_artist))

        spotify_dict_temp = copy.copy(spotify_dict)
        itunes_dict_temp = copy.copy(itunes_dict)

        for song in spotify_dict.keys():
            song_temp = song
            if "(Original Mix)" in song:
                song_temp.replace("(Original Mix)","")
            if song or song_temp in itunes_dict.keys():
                spotify_dict_temp.pop(song)
                itunes_dict_temp.pop(song)

        with open('leftovers/' + spotify_playlist + '_spotify.csv', 'wt+', errors='ignore',
        newline='') as f:
            for key in spotify_dict_temp.keys():
                f.write("%s, %s\n" % (key, spotify_dict_temp[key]))
        print ("made leftover spotify playlist for: " + spotify_playlist)
            
        with open('leftovers/' + itunes_playlist + '_itunes.csv', 'wt+', errors='ignore',
        newline='') as f:
            for key in itunes_dict_temp.keys():
                f.write("%s, %s\n" % (key, itunes_dict_temp[key]))
        print ("made leftover itunes playlist for: " + itunes_playlist)
