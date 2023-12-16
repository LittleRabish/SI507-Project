from movie_graph import create_movie_graph, get_recommendations
from youtube import search_youtube
import random
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns

INVALID_INPUT = "Invalid input! Please enter again."
GENRES = {"1": "Action", "2": "Adventure", "3": "Animation", "4": "Comedy", "5": "Crime",
          "6":"Documentary", "7": "Drama", "8": "Family", "9": "Fantasy", "10": "History",
          "11": "Horror", "12": "Music", "13": "Mystery", "14": "Romance", "15": "Science Fiction",
          "16": "TV Movie", "17": "Thriller", "18": "War", "19": "Western"}
GENRE_PROMPT = """Which genre do you like? Please enter the number representing each genre:
(1: Action, 2: Adventure, 3: Animation, 4: Comedy, 5: Crime,
6: Documentary, 7: Drama, 8: Family, 9: Fantasy, 10: History,
11: Horror, 12: Music, 13: Mystery, 14: Romance, 15: Science Fiction,
16: TV Movie, 17: Thriller, 18: War, 19: Western)\n"""
YEARS = {"1": (2020, 2023), "2": (2010, 2019), "3": (2000, 2009),
         "4": (1990, 1999), "5": (1800, 1989)}
YEAR_PROMPT = """What about the release time?
(1: 2020-2023, 2: 2010-2019, 3: 2000-2009, 4: 1990-1999, 5: -1989)\n"""
BASIC_MOVIES = ["897087", "901362", "466420", "1075794", "787699", "872585", "566810", "1001835", "507089", "479753", "670292", "951546", "385687", "1046032", "854648", "1047925", "575264", "299054", "609681", "695721", "940721", "502356", "662167", "775244", "10908", "8871", "936059", "1022964", "920258", "926393", "569094", "656156", "960481", "667538", "753342", "76600", "360920", "615656", "603692", "287903", "238", "278", "240", "424", "19404", "389", "129", "496243", "155", "497", "372058", "680", "122", "13", "429", "769", "12477", "637", "346", "11216", "667257", "550", "696374", "568332", "539", "598", "311", "372754", "724089", "157336", "510", "620249", "761053", "40096", "324857", "120", "4935", "569094", "14537", "378064"]


def plot_results(rcmds: list) -> None:
    titles = [movie.title for movie in rcmds]
    votes = [movie.vote_avg for movie in rcmds]
    popularities = [movie.popularity for movie in rcmds]
    # plt.figure(figsize=(12, 6))
    sns.scatterplot(x=titles, y=votes, size=popularities, sizes=(50, 500))
    plt.ylabel('Vote Average')
    plt.ylim(5, 10)
    plt.xlabel('Movies')
    plt.xticks(rotation=45)
    plt.legend(title='Popularity')
    plt.show()


graph = create_movie_graph("movies.json")

print("Would you like to watch some movies?")
while True:
    try:
        genre_id = input(GENRE_PROMPT)
        genre = GENRES[genre_id]
        year_id = input(YEAR_PROMPT)
        year = YEARS[year_id]
        break
    except:
        print(INVALID_INPUT)
rcmds = get_recommendations(graph, random.choice(BASIC_MOVIES), genre, year[0], year[1])
if len(rcmds) == 0:
    rcmds = get_recommendations(graph, random.choice(BASIC_MOVIES), genre, year[0], year[1])
print("Here are some recommendations for you:")
for i, movie in enumerate(rcmds, start=1):
    print(f"{i} {movie.title}({movie.release_date[:4]})")

plot_flag = input("Would you like to look at the ratings & popularity scores? (1: yes, 2: no)\n")
if plot_flag == "1":
    plot_results(rcmds)

prefer_movie = input("Are you interested in any movie above? Please enter the number.\n")
while True:
    try:
        prefer_id = rcmds[int(prefer_movie)-1].id
        prefer_title = rcmds[int(prefer_movie)-1].title
        
        youtube_flag = input("Would you like to look at some related video clips from YouTube? (1: yes, 2: no)\n")
        if youtube_flag == "1":
            urls = search_youtube(prefer_title)
            for title, url in urls.items():
                print(url, title)
        
        rcmd_flag = input("Would you like to get more recommendations? (1: yes, 2: no)\n")
        if rcmd_flag == "1":
            rcmds = get_recommendations(graph, prefer_id, genre, year[0], year[1])
            print("Here are some recommendations for you:")
            for i, movie in enumerate(rcmds, start=1):
                print(f"{i} {movie.title}({movie.release_date[:4]})")
    except:
        print(INVALID_INPUT)
    
    prefer_movie = input("Any other movie you want to learn more about? Please enter the number. Or you can enter 0 to quit.\n")
    if prefer_movie == "0":
        break
