import json
from collections import deque

class Movie_Vertex:
    def __init__(self, movie_id: str, movie_info: dict) -> None:
        self.id = movie_id
        self.title = movie_info["title"]
        self.release_date = movie_info["release_date"]
        self.genres = []
        for genre in movie_info["genres"]:
            self.genres.append(genre["name"])
        self.popularity = movie_info["popularity"]
        self.vote_avg = movie_info["vote_avg"]
        nbrs = [str(id) for id in movie_info["connected_to"]]
        self.connected_to = set(nbrs)

    def add_neighbor(self, nbr_movie_id: str) -> None:
        """when the connection in cached file is unidirectional"""
        # if nbr_movie_id not in self.connected_to:
        #     print(self.id, "<->", nbr_movie_id)
        self.connected_to.add(nbr_movie_id)
    
    def get_connections(self) -> list:
        return self.connected_to
    
    def __str__(self) -> str:
        return str(self.id) + " is connected to " + str([nbr for nbr in self.connected_to])


class Movie_Graph:
    def __init__(self) -> None:
        self.vert_list = {}
    
    def add_vertex(self, movie_id: str, movie_info: dict) -> Movie_Vertex:
        new_vertex = Movie_Vertex(movie_id, movie_info)
        self.vert_list[movie_id] = new_vertex
        return new_vertex
    
    def get_vertex(self, movie_id: str) -> Movie_Vertex:
        if movie_id in self.vert_list:
            return self.vert_list[movie_id]
        else:
            raise KeyError(movie_id, " not in graph")
    
    def add_edge(self, movie_id_1: str, movie_id_2: str) -> None:
        """must create vertex before adding edge"""
        self.vert_list[movie_id_1].add_neighbor(movie_id_2)
        self.vert_list[movie_id_2].add_neighbor(movie_id_1)
    
    def __iter__(self):
        return iter(self.vert_list.values())


def create_movie_graph(file_name: str) -> Movie_Graph:
    """Load the data in as a graph.

    Parameters
    ----------
    file_name: str
        The name of the file to be loaded.

    Returns
    -------
    Movie_Graph
        A graph representing movies and their relationships.

    """
    with open(file_name, "r") as f:
        movies_json = f.read()
        movies = json.loads(movies_json)
    # print(len(movies), "movies loaded")
    
    graph = Movie_Graph()
    for movie_id, movie_info in movies.items():
        graph.add_vertex(movie_id, movie_info)
    
    # Make sure the connection exists in the nbr list of both movies
    for movie_i in graph:
        for movie_j_id in movie_i.get_connections():
            graph.add_edge(movie_i.id, movie_j_id)
    
    return graph

def get_recommendations(graph: Movie_Graph, start_movie_id: str,
                       genre: str, year_min: int, year_max: int) -> list:
    """use BFS to search the movie graph and get a list of recommended movies"""
    visited = set()
    q = deque()
    rcmds = []
    
    visited.add(start_movie_id)
    q.append(start_movie_id)

    while q:
        current_id = q.popleft()
        current_vertex = graph.get_vertex(current_id)
        year_str = current_vertex.release_date[:4]
        if year_str == "":
            year = 0
        else:
            year = int(current_vertex.release_date[:4])

        if genre in current_vertex.genres and year >= year_min and year <= year_max:
            # print(current_vertex.id, current_vertex.title)
            rcmds.append(current_vertex)
        if len(rcmds) == 8:
            return rcmds

        for nbr_id in current_vertex.get_connections():
            if nbr_id not in visited:
                visited.add(nbr_id)
                q.append(nbr_id)
    
    return rcmds


if __name__ == "__main__":
    graph = create_movie_graph("movies.json")
    # for movie_id in graph.get_vertex("161445").connected_to:
    #     print(type(movie_id))
    get_recommendations(graph, "37165", "Animation", 2000, 2009)