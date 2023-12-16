import requests
from api_keys import YOUTUBE_KEY

def search_youtube(query: str) -> dict:
    """
    use the YouTube API to search for videos matching the movie title

    return a dictionary with video title as key, and url link as value
    """
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {"key": YOUTUBE_KEY,
              "part": "snippet",
              "type": "video",
              "q": query,
              "maxResults": 10}
    response = requests.get(url, params=params)
    results = response.json()
    # print(json.dumps(results, indent=2))

    results_url = {}
    for video in results["items"]:
        title = video["snippet"]["title"]
        video_id = video["id"]["videoId"]
        results_url[title] = f'https://youtu.be/{video_id}'

    return results_url


if __name__ == "__main__":
    print(search_youtube("Beau Travail"))