from youtube.youtube_recommender import YouTubeRecommender


API_KEY = "AIzaSyBljiPMNaU4CTdFqgLmfXcEnP06jwLoVGU"


youtube = YouTubeRecommender(
    API_KEY
)


test_moods = [
    "happy",
    "sad",
    "angry",
    "neutral"
]


for mood in test_moods:

    print("\n" + "=" * 50)

    print(f"🎭 MOOD: {mood.upper()}")

    print("=" * 50)

    results = youtube.search_by_mood(
        mood,
        number_of_results=3
    )

    for index, song in enumerate(
        results,
        start=1
    ):

        print(
            f"\n{index}. {song['title']}"
        )

        print(
            f"   🎤 {song['channel']}"
        )

        print(
            f"   🔗 {song['url']}"
        )