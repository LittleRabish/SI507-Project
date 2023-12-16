# SI507-Project

The goal of this project is to create a movie recommendation system that leverages data from The Movie Database (TMDB) API and YouTube Data API. By combining comprehensive movie information from TMDB with video clips from YouTube, users can conveniently preview movies before making viewing decisions.

## To Run the Program

1. Make sure you have the following packages installed:
   - `requests`
   - `matplotlib`
   - `seaborn`
2. My own API keys for TMDB and YouTube are used in the program. If they are invalid, please replace them with your own keys in `api_keys.py`.
3. Get the code `main.py`, `movie_graph.py`, `youtube.py`, `api_keys.py`, and the cached data `movies.json` ready in the same directory.
4. Run `main.py` and interact with the program in the command line.

## Data Structure

The movies are organized into a graph. All the movie details, including the related movies, are stored as a vertex. The edge exists between two movies if either movie appears in the "connected_to" list of the other movie. Since most of the connections between movies are obtained during the caching process, no other json file will be used to store the graph structure. The graph is constructed directly from the cached data `movies.json`, and represented as a `Movie_Graph` object in `movie_graph.py`.

## Caching

The code in `caching_tmdb.py` is used to cache the data from TMDB.
