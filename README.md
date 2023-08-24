# recommusic

This project is a music recommendation engine that leverages natural language processing (NLP) techniques to suggest music based on album reviews. The project is developed with Python, SQLite, and Flask, utilizing a pre-trained model for generating embeddings from the text of music reviews.

<img src="assets/search_results.png" alt="Search results" width="300"/>
<img src="assets/review.png" alt="Review" width="300"/>

## Features

- View album details including artist, album name, year released, rating, review, reviewer, genre, label, and release date.
- Search for albums or artists.
- Get recommended albums based on the text of the review.

## How It Works

The recommendation engine operates by transforming the album reviews text into vector embeddings using a pre-trained model. These embeddings are then stored in a SQLite database along with other album details.

When a user views an album, the application calculates the similarity score based on multiple factors including cosine similarity of their review embeddings, artist similarity, label similarity, genre similarity, and year similarity. This score is a weighted combination of these factors which include:

- Cosine similarity of the review embeddings multiplied by the album rating.
- If the artist is the same as the selected album.
- If the label is the same as the selected album.
- If the genre is the same as the selected album.
- An inverse value based on the absolute difference in release year.

The application then presents the most similar albums to the user based on this combined score.

## License

Distributed under the MIT License. See `LICENSE` for more information.
