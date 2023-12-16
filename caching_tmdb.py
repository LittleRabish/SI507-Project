import requests
import json
from collections import Counter


def get_basic_movies(order_by: str, limit: int):
    """Use the "popular"/"top rated" functions of the TMDB API
    to get a list of movies as the base vertices to be expanded

    Parameters
    ----------
    order_by: str
        The list of movies are ordered by popularity("popular")/rating("top_rated").
    limit: int
        the number of movies to return

    Returns
    -------
    list
        a list of movie ids

    """
    url = "https://api.themoviedb.org/3/movie/" + order_by
    params = {"api_key": "627a016b527c977f26aa27243b1cf682",
              "page": 1}
    movie_ids = []
    while len(movie_ids) < limit:
        print(params["page"])
        response = requests.get(url, params=params)
        results = response.json()
        for movie in results["results"]:
            movie_ids.append(movie["id"])
        params["page"] += 1
    return movie_ids


def find_related_movies(movie_ids: list, movies: dict):
    """use the movie ids found in latest iteration to find more related movie ids,
    as well as retrieve the details of the movie ids found in last iteration

    Parameters
    ----------
    movie_ids: list
        The movie ids in the latest iteration.
    movies: dict
        All movies with cached details.

    Returns
    -------
    list
        a list of new movie ids
    movies: dict
        Updated movies with cached details.

    """
    related_movies = set()
    for it, movie_id in enumerate(movie_ids):
        url = f"https://api.themoviedb.org/3/movie/{movie_id}"
        params = {"api_key": "627a016b527c977f26aa27243b1cf682",
                  "append_to_response": "similar,recommendations"}
        response = requests.get(url, params=params)
        results = response.json()
        # print(json.dumps(results, indent=2))
        connected_to = set()
        for i, rec_movie in enumerate(results["recommendations"]["results"]):
            if i < 6:
                connected_to.add(rec_movie["id"])
            else:
                break
        for i, sim_movie in enumerate(results["similar"]["results"]):
            if i < 6:
                connected_to.add(sim_movie["id"])
            else:
                break
        related_movies = related_movies | connected_to

        details = {"title": results["title"],
                   "release_date": results["release_date"],
                   "genres": results["genres"],
                   "popularity": results["popularity"],
                   "vote_avg": results["vote_average"],
                   "connected_to": list(connected_to)}
        movies[movie_id] = details
        print(it)

    return list(related_movies), movies


def complete_last_iteration(last_it_ids: list, all_movie_ids: set, movies: dict):
    """retrieve the details of the movie ids found in the last iteration

    Parameters
    ----------
    last_it_ids: list
        The movie ids in the last iteration.
    all_movie_ids: set
        The set of all movie ids.
    movies: dict
        All movies with cached details.

    Returns
    -------
    movies: dict
        Updated final version of movies with cached details.

    """
    for it, movie_id in enumerate(last_it_ids):
        if movie_id not in movies:
            url = f"https://api.themoviedb.org/3/movie/{movie_id}"
            params = {"api_key": "627a016b527c977f26aa27243b1cf682",
                      "append_to_response": "similar,recommendations"}
            response = requests.get(url, params=params)
            results = response.json()
            # print(json.dumps(results, indent=2))
            connected_to = set()
            for rec_movie in results["recommendations"]["results"]:
                if rec_movie["id"] in all_movie_ids:
                    connected_to.add(rec_movie["id"])
            for sim_movie in results["similar"]["results"]:
                if sim_movie["id"] in all_movie_ids:
                    connected_to.add(sim_movie["id"])

            details = {"title": results["title"],
                    "release_date": results["release_date"],
                    "genres": results["genres"],
                    "popularity": results["popularity"],
                    "vote_avg": results["vote_average"],
                    "connected_to": list(connected_to)}
            movies[movie_id] = details
            print(it, connected_to)

    return movies


def save_movie_details(movies: dict) -> None:
    movies_json = json.dumps(movies, indent=2)
    with open("movies.json", "w") as fw:
        fw.write(movies_json)

def load_movie_details() -> dict:
    with open("movies.json", "r") as f:
        movies_json = f.read()
        movies = json.loads(movies_json)
    print(len(movies), "movies loaded")
    return movies

def save_movie_ids(movie_ids: dict) -> None:
    movie_ids_json = json.dumps(movie_ids, indent=2)
    with open("movie_ids.json", "w") as fw:
        fw.write(movie_ids_json)

def load_movie_ids() -> dict:
    with open("movie_ids.json", "r") as f:
        movie_ids_json = f.read()
        movie_ids = json.loads(movie_ids_json)
    all_movie_ids = []
    for id_list in movie_ids.values():
        all_movie_ids += id_list
    print(len(set(all_movie_ids)), "movie ids scraped")
    return movie_ids


if __name__ == "__main__":
    movie_ids = {}
    movies = {}
    
    movie_ids = load_movie_ids()
    all_movie_ids = []
    for id_list in movie_ids.values():
        all_movie_ids += id_list
    movies = load_movie_details()
    # print(len(movie_ids["basic"])) # 80
    # print(len(set(movie_ids["basic"]))) # 79
    # print(len(movie_ids["1it"])) # 590
    # print(len(movie_ids["2it"])) # 2779
    
    basic, new_it, last_it = False, False, False

    if basic: # ===== get basic movies =====
        basic_movies = get_basic_movies("popular", 40)
        basic_movies += get_basic_movies("top_rated", 40)
        movie_ids["basic"] = basic_movies
    elif new_it: # ===== new iteration =====
        new_movie_ids, movies = find_related_movies(movie_ids["1it"], movies)
        print(len(new_movie_ids))
        movie_ids["2it"] = new_movie_ids
    elif last_it: # ===== last iteration =====
        movies = complete_last_iteration(movie_ids["2it"], set(all_movie_ids), movies)

    # print(Counter(all_movie_ids))
    # print(len(set(all_movie_ids)))
    # print(len(movies)) # 2906

    save_movie_ids(movie_ids)
    save_movie_details(movies)