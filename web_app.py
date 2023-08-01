from flask import Flask, render_template, request, url_for, g
import sqlite3
from embeddings import get_similar_albums

app = Flask(__name__)
DATABASE = 'reviews.db'  # replace with your db path
PER_PAGE = 9  # number of reviews per page

def get_db():
  db = getattr(g, '_database', None)
  if db is None:
    db = g._database = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
  return db

@app.teardown_appcontext
def close_connection(exception):
  db = getattr(g, '_database', None)
  if db is not None:
    db.close()

@app.route('/')
def home():
  page = request.args.get('page', 1, type=int)
  offset = (page - 1) * PER_PAGE
  cur = get_db().cursor()
  cur.execute(f"SELECT * FROM reviews LIMIT {PER_PAGE} OFFSET {offset}")
  reviews = cur.fetchall()
  cur.execute('SELECT COUNT(*) FROM reviews')
  total = cur.fetchone()[0]
  next_url = url_for('home', page=page + 1) if offset + PER_PAGE < total else None
  prev_url = url_for('home', page=page - 1) if page > 1 else None
  return render_template('home.html', reviews=reviews, next_url=next_url, prev_url=prev_url)

@app.route('/review/<string:artist>/<string:album>')
def review(artist, album):
  cur = get_db().cursor()
  cur.execute(f"SELECT * FROM reviews WHERE artist = '{artist}' AND album = '{album}'")
  review = cur.fetchone()
  similar_albums = get_similar_albums(review[0])
  return render_template('review.html', review=review, similar_albums=similar_albums)

@app.route('/search', methods=['POST'])
def search():
  query = request.form.get('q')
  cur = get_db().cursor()
  cur.execute(f"SELECT * FROM reviews WHERE artist LIKE '%{query}%' OR album LIKE '%{query}%'")
  results = cur.fetchall()
  return render_template('search_results.html', results=results)


if __name__ == '__main__':
  app.run(debug=True)
