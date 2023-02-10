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

algorithim = 0
if algorithim:
    for spotify_playlist in spotify_list:
        print("spotify playlist : " + spotify_playlist)
        itunes_playlist = spotify_playlist
        if itunes_playlist in itunes_list:
            spotify_csv = pd.read_csv('spotify_playlists/' + spotify_playlist + '.csv')
            spotify_song_list = spotify_csv['name'].tolist()
            spotify_song_list.sort()

            itunes_csv = pd.read_csv('itunes_playlists/' + itunes_playlist + '.csv', header=None)
            itunes_song_list = itunes_csv[itunes_csv.columns[0]].tolist()
            itunes_song_list.sort()
            spotify_missing_list = []
            itunes_missing_list = []

            with open('ogs/' + spotify_playlist + '_spotify.csv', 'wt+', errors='ignore',
            newline='') as f:
                for item in spotify_song_list:
                    f.write(f"{item}\n")
            print ("made leftover spotify playlist for: " + spotify_playlist)
                
            with open('ogs/' + itunes_playlist + '_itunes.csv', 'wt+', errors='ignore',
            newline='') as f:
                for item in itunes_song_list:
                    f.write(f"{item}\n")
            print ("made leftover itunes playlist for: " + itunes_playlist)

            for spotify_song in spotify_song_list:
                song_check = 1
                failed_check = 1
                i = 0
                if " - " in spotify_song:
                    song_split = spotify_song.split(' - ')
                    song_temp = song_split[0] + " (" + song_split[1] + ")"
                    dash_check = 1
                else:
                    dash_check = 0
                while song_check and failed_check:
                    if len(itunes_song_list) == i:
                        failed_check = 0
                        song_check = 0
                    else:
                        if dash_check:
                            if song_temp in itunes_song_list[i]:
                                if 'remix' in song_split[1]:
                                    if 'remix' in itunes_song_list[i]:
                                        itunes_song_list.pop(i)
                                        song_check = 0
                                else:
                                        itunes_song_list.pop(i)
                                        song_check = 0                                                 
                        else:
                            if spotify_song in itunes_song_list[i]:
                                if not 'remix' in itunes_song_list[i]:
                                    itunes_song_list.pop(i)
                                    song_check = 0
                        i = i + 1

                if not failed_check:
                    if dash_check:
                        spotify_missing_list.append(song_temp)
                    else:
                        spotify_missing_list.append(spotify_song)


            with open('leftovers/' + spotify_playlist + '_spotify.csv', 'wt+', errors='ignore',
            newline='') as f:
                for item in spotify_missing_list:
                    f.write(f"{item}\n")
            print ("made leftover spotify playlist for: " + spotify_playlist)
                
            with open('leftovers/' + itunes_playlist + '_itunes.csv', 'wt+', errors='ignore',
            newline='') as f:
                for item in itunes_song_list:
                    f.write(f"{item}\n")
            print ("made leftover itunes playlist for: " + itunes_playlist)
            
else:
    for spotify_playlist in spotify_list:
        print("spotify playlist : " + spotify_playlist)
        itunes_playlist = spotify_playlist
        if itunes_playlist in itunes_list:
            spotify_csv = pd.read_csv('spotify_playlists/' + spotify_playlist + '.csv')
            spotify_song_temp = spotify_csv['name'].tolist()

            spotify_artist = spotify_csv['artist'].tolist()

            itunes_csv = pd.read_csv('itunes_playlists/' + itunes_playlist + '.csv', header=None)
            itunes_song_list = itunes_csv[itunes_csv.columns[0]].tolist()
            artist_matrix = itunes_csv[itunes_csv.columns[1]].to_numpy()
            itunes_artist = artist_matrix.tolist()

            spotify_dict = dict(zip(spotify_song_temp, spotify_artist))
            spotify_dict = dict(sorted(spotify_dict.items()))
            itunes_dict = dict(zip(itunes_song_list, itunes_artist))
            itunes_dict = dict(sorted(itunes_dict.items()))

            spotify_dict_temp = copy.copy(spotify_dict)
            spotify_dict_temp = dict(sorted(spotify_dict_temp.items()))
            itunes_dict_temp = copy.copy(itunes_dict)
            itunes_dict_temp = dict(sorted(itunes_dict_temp.items()))

            for song in spotify_dict.keys():
                song_temp = song
                if "(Original Mix)" in song:
                    song_temp.replace("(Original Mix)","")
                if "(Extended Mix)" in song:
                    song_temp.replace("(Extended Mix)","")
                if song in itunes_dict.keys() or song_temp in itunes_dict.keys():
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