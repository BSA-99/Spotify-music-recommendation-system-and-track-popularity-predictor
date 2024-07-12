import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import joblib

# Replace with your own Client ID and Client Secret
CLIENT_ID = 'your_client_id'
CLIENT_SECRET = 'your_client_secret'

auth_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(auth_manager=auth_manager)

def get_song_features(track_id):
    try:
        track = sp.track(track_id)
        if track is None:
            print(f"Track ID {track_id} does not exist.")
            return None
        audio_features = sp.audio_features(track_id)[0]
        if audio_features:
            features = [
                audio_features['danceability'],
                audio_features['energy'],
                audio_features['key'],
                audio_features['loudness'],
                audio_features['mode'],
                audio_features['speechiness'],
                audio_features['acousticness'],
                audio_features['instrumentalness'],
                audio_features['liveness'],
                audio_features['valence'],
                audio_features['tempo']
            ]
            return features
        else:
            print(f"No audio features found for track ID {track_id}.")
            return None
    except Exception as e:
        print(f"Error fetching features for track ID {track_id}: {e}")
        return None

def predict_popularity(song_features, scaler, model):
    song_features_scaled = scaler.transform([song_features])
    prediction = model.predict(song_features_scaled)
    return prediction[0]

def predict_new_song_popularity(track_id, scaler, model):
    song_features = get_song_features(track_id)
    if song_features:
        predicted_popularity = predict_popularity(song_features, scaler, model)
        return predicted_popularity
    else:
        print("Could not fetch the features for the track.")
        return None
