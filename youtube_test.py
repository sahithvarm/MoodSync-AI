from googleapiclient.discovery import build


API_KEY = "AIzaSyBljiPMNaU4CTdFqgLmfXcEnP06jwLoVGU"


youtube = build(
    "youtube",
    "v3",
    developerKey=API_KEY
)


request = youtube.search().list(
    part="snippet",
    q="happy Telugu songs",
    type="video",
    maxResults=5
)


response = request.execute()


for item in response["items"]:

    video_id = item["id"]["videoId"]
    title = item["snippet"]["title"]

    print("\n🎵", title)
    print("https://www.youtube.com/watch?v=" + video_id)