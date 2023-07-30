import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import sqlite3

def get_db():
  conn = sqlite3.connect('../pitchfork/reviews.db')
  conn.row_factory = sqlite3.Row  # This allows access to column by name
  return conn

def load_embeddings():
  with open('embeddings.pkl', 'rb') as f:
    data = pickle.load(f)
  return data

def get_similar_albums(target_embedding, artist, album, n_similar=9):
  # Load embeddings
  with open('embeddings.pkl', 'rb') as f:
    data = pickle.load(f)

  embeddings = data['embeddings']
  albums = data['albums']
  artists = data['artists']

  # Calculate cosine similarities
  similarities = cosine_similarity([target_embedding], embeddings)[0]

  # Get indices of albums sorted by similarity
  sorted_indices = np.argsort(similarities)[::-1]

  # Get details of similar albums
  similar_albums = []
  for idx in sorted_indices:
    # Exclude the album itself
    if artists[idx] == artist and albums[idx] == album:
      continue

    # Fetch album details from database
    cur = get_db().cursor()
    cur.execute(
      "SELECT * FROM reviews WHERE artist = ? AND album = ?",
      (artists[idx], albums[idx])
    )
    album_details = cur.fetchone()

    similar_albums.append(album_details)

    if len(similar_albums) == n_similar:
      break

  return similar_albums
