#!/usr/bin/env python
# coding: utf-8

# In[13]:


import os
import datetime

import pandas as pd
import matplotlib.pyplot as plt

import ipywidgets as widgets
from ipywidgets import interact


# In[24]:


# GATHER ALL THE DATA

path_to_json = 'C:/Users/Tam/Desktop/Spotify/'
frames = []
for file_name in [file for file in os.listdir(path_to_json) if file.endswith('.json')]:
    frames.append(pd.read_json(path_to_json + file_name))

complete_df = pd.concat(frames)
complete_df


# In[25]:


# SANETIZE DATA

df = complete_df.copy()

# drop all rows containing podcasts
df = df[df['spotify_track_uri'].notna()]

# drop all songs which were playing less than 15 seconds
df = df[df['ms_played'] > 15000]

# convert ts from string to datetime
df['ts'] = pd.to_datetime(df['ts'], utc=False)
df['date'] = df['ts'].dt.date

# drop all columns which are not needed
columns_to_keep = [
    'ts',
    'date',
    'ms_played',
    'platform',
    'conn_country',
    'master_metadata_track_name',
    'master_metadata_album_artist_name',
    'master_metadata_album_album_name',
    'spotify_track_uri'
]
df = df[columns_to_keep]

df = df.sort_values(by=['ts'])
songs_df = df.copy()
songs_df


# In[26]:


# TOP SONGS OF ALL TIME

df = songs_df.copy()


df = df.groupby(['spotify_track_uri']).size(
).reset_index().rename(columns={0: 'count'})
df = df.sort_values(by=['count'], ascending=False).reset_index()

df = df.merge(songs_df.drop_duplicates(subset='spotify_track_uri'))
df = df[['master_metadata_track_name', 'master_metadata_album_artist_name', 'master_metadata_album_album_name', 'count']]
df.head(20)


# In[27]:


# TOP SONGS IN 2023

def top_songs_in_year(year):
    df = songs_df.copy()

    df['year'] = df['ts'].dt.year

    df = df.loc[(df['year'] == year)]

    print(
        f"Time listened in {year}: {datetime.timedelta(milliseconds=int(df['ms_played'].sum()))}")

    df = df.groupby(['spotify_track_uri']).size(
    ).reset_index().rename(columns={0: 'count'})
    df = df.sort_values(by=['count'], ascending=False).reset_index()

    df = df.merge(songs_df.drop_duplicates(subset='spotify_track_uri'))
    df = df[['master_metadata_track_name',
             'master_metadata_album_artist_name',
             'master_metadata_album_album_name',
             'count']]

    return df.head(20)


top_songs_in_year(2023)


# In[ ]:




