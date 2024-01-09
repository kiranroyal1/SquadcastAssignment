import pandas as pd
import psycopg2
from sqlalchemy import create_engine

# Replace the following with your PostgreSQL connection details
db_connection = {
    'host': 'localhost',
    'database': 'movies',
    'user': 'postgres',
    'password': 'kiran4',
    'port': '5432'
}
engine = create_engine(f"postgresql+psycopg2://{db_connection['user']}:{db_connection['password']}@{db_connection['host']}:{db_connection['port']}/{db_connection['database']}")

# Replace 'your_username', 'your_password', 'your_host', and 'your_database' with your PostgreSQL credentials
# engine = create_engine('postgresql://your_username:your_password@your_host/your_database')

# Load 'movies' table into a pandas DataFrame
movies_query = "SELECT * FROM movies"
movies_df = pd.read_sql(movies_query, engine)

# Load 'ratings' table into a pandas DataFrame
ratings_query = "SELECT * FROM ratings"
ratings_df = pd.read_sql(ratings_query, engine)

# print("Columns in df_movies:", movies_df.columns)
# print("Columns in df_ratings:", ratings_df.columns)

# Task a: Top 5 Movie Titles
# Sort by duration
top_duration = movies_df.sort_values(by='minutes', ascending=False).head(5)
print("Top 5 Movies by Duration:")
print(top_duration[['title', 'minutes']])

# Sort by year of release
top_year = movies_df.sort_values(by='year', ascending=False).head(5)
print("\nTop 5 Movies by Year of Release:")
print(top_year[['title', 'year']])

# Filter movies with minimum 5 ratings
avg_ratings_df = ratings_df.groupby('movie_id')['rating'].agg(['mean', 'count']).reset_index()
avg_ratings_df = avg_ratings_df[avg_ratings_df['count'] >= 5]
# top_avg_ratings = movies_df.merge(avg_ratings_df, on='movie_id').sort_values(by='mean', ascending=False).head(5)
# print("\nTop 5 Movies by Average Rating (with minimum 5 ratings):")
# print(top_avg_ratings[['title', 'mean', 'count']])

# Task b: Number of Unique Raters
unique_raters_count = ratings_df['rater_id'].nunique()
print(f"\nNumber of Unique Raters: {unique_raters_count}")

# Task c: Top 5 Rater IDs
# Most movies rated
top_raters_movie_count = ratings_df['rater_id'].value_counts().head(5)
print("\nTop 5 Rater IDs by Most Movies Rated:")
print(top_raters_movie_count)

# Highest average rating given (consider raters with min 5 ratings)
raters_avg_rating_df = ratings_df.groupby('rater_id')['rating'].agg(['mean', 'count']).reset_index()
raters_avg_rating_df = raters_avg_rating_df[raters_avg_rating_df['count'] >= 5]
top_raters_avg_rating = raters_avg_rating_df.sort_values(by='mean', ascending=False).head(5)
print("\nTop 5 Rater IDs by Highest Average Rating (with minimum 5 ratings):")
print(top_raters_avg_rating[['rater_id', 'mean', 'count']])

# Task d: Top Rated Movie
top_rated_movie_director = movies_df[(movies_df['director'] == 'Michael Bay')].sort_values(by='avg_rating', ascending=False).head(1)
print("\nTop Rated Movie by Director 'Michael Bay':")
print(top_rated_movie_director[['title', 'avg_rating']])

top_rated_movie_comedy = movies_df[(movies_df['genre'] == 'Comedy')].sort_values(by='avg_rating', ascending=False).head(1)
print("\nTop Rated Comedy Movie:")
print(top_rated_movie_comedy[['title', 'avg_rating']])

top_rated_movie_2013 = movies_df[(movies_df['year'] == 2013)].sort_values(by='avg_rating', ascending=False).head(1)
print("\nTop Rated Movie in the year 2013:")
print(top_rated_movie_2013[['title', 'avg_rating']])

top_rated_movie_india = movies_df[(movies_df['country'] == 'India') & (movies_df['rating_count'] >= 5)].sort_values(by='avg_rating', ascending=False).head(1)
print("\nTop Rated Movie in India (with minimum 5 ratings):")
print(top_rated_movie_india[['title', 'avg_rating']])

# Task e: Favorite Movie Genre of Rater ID 1040
rater_1040_favorite_genre = ratings_df[ratings_df['rater_id'] == 1040].merge(movies_df, on='movie_id')
favorite_genre = rater_1040_favorite_genre['genre'].value_counts().idxmax()
print(f"\nFavorite Movie Genre of Rater ID 1040: {favorite_genre}")

engine.dispose()
