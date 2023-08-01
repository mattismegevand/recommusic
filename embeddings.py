import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import sqlite3

embeddings = np.load('embeddings.npy')

def get_db():
  conn = sqlite3.connect('reviews.db')
  conn.row_factory = sqlite3.Row  # This allows access to column by name
  return conn

def select_album(id):
  cur = get_db().cursor()
  cur.execute('SELECT * FROM reviews WHERE id = ?', (id,))
  return cur.fetchone()

def select_a_col(col):
  cur = get_db().cursor()
  cur.execute(f"SELECT {col} FROM reviews")
  rows = cur.fetchall()
  return [row[col] for row in rows]

def get_similar_albums(id_embedding, n_similar=9):
  album = select_album(id_embedding)
  ratings = np.array(select_a_col('rating'))
  artist_sims = np.array([1 if a == album['artist'] else 0 for a in select_a_col('artist')])
  labels_sims = np.array([1 if a == album['label'] else 0 for a in select_a_col('label')])
  genres_sims = np.array([1 if a == album['genre'] else 0 for a in select_a_col('genre')])
  year_sims = np.array([1 / (abs(a - album['year_released']) + 1) for a in select_a_col('year_released')])

  similarities = cosine_similarity([embeddings[id_embedding]], embeddings).flatten()
  similarities *= (ratings / 10)
  similarities += artist_sims + labels_sims + genres_sims + year_sims

  sorted_indices = np.argsort(similarities)[::-1]

  similar_albums = []
  for idx in sorted_indices:
    # exclude the album itself
    if idx == id_embedding - 1:
      continue

    cur = get_db().cursor()
    cur.execute(f"SELECT * FROM reviews WHERE id = {idx + 1}")

    album_details = cur.fetchone()
    similar_albums.append(album_details)
    if len(similar_albums) == n_similar:
      break

  return similar_albums
