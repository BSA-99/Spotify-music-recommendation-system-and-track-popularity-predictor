import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

# Replace with your own Client ID and Client Secret
CLIENT_ID = '59513a4da7484f4892407bbf640f57cd'
CLIENT_SECRET = '0387708098a94de9b1cccef3aeff0b5b'

# Initialize Spotify API client without cache management
auth_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(auth_manager=auth_manager)

# List of track IDs (you can get this from various Spotify playlists or your own selection)
track_ids = [
    '3n3Ppam7vgaVa1iaRUc9Lp',  # Example track ID, add more track IDs
    '7ouMYWpwJ422jRcDASZB7P',
    # Add more track IDs here
]

# Function to fetch track details and audio features
def fetch_track_data(track_id):
    try:
        track = sp.track(track_id)
        if track is None:
            print(f"Track ID {track_id} does not exist.")
            return None
        audio_features = sp.audio_features(track_id)[0]
        if audio_features:
            data = {
                'Track ID': track_id,
                'Track Name': track['name'],
                'Artists': ', '.join([artist['name'] for artist in track['artists']]),
                'Popularity': track['popularity'],
                'Danceability': audio_features['danceability'],
                'Energy': audio_features['energy'],
                'Key': audio_features['key'],
                'Loudness': audio_features['loudness'],
                'Mode': audio_features['mode'],
                'Speechiness': audio_features['speechiness'],
                'Acousticness': audio_features['acousticness'],
                'Instrumentalness': audio_features['instrumentalness'],
                'Liveness': audio_features['liveness'],
                'Valence': audio_features['valence'],
                'Tempo': audio_features['tempo']
            }
            return data
        else:
            print(f"No audio features found for track ID {track_id}.")
            return None
    except spotipy.exceptions.SpotifyException as e:
        print(f"Error fetching data for track ID {track_id}: {e}")
        return None

# Ensure the data directory exists
os.makedirs('data', exist_ok=True)

# Fetch data for all track IDs
tracks_data = []
for track_id in track_ids:
    track_data = fetch_track_data(track_id)
    if track_data:
        tracks_data.append(track_data)

# Convert to DataFrame and save as CSV
df = pd.DataFrame(tracks_data)
df.to_csv('data/dataset.csv', index=False)
print("Data saved to data/dataset.csv")
