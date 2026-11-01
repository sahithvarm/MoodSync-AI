from collections import Counter, deque


class EmotionStabilizer:

    def __init__(self, history_size=7):

        self.history_size = history_size

        self.emotion_history = deque(
            maxlen=history_size
        )


    def update(self, emotion):

        if not emotion:
            return None

        # Add the latest emotion
        self.emotion_history.append(emotion)

        # Find the most frequently detected emotion
        emotion_counts = Counter(
            self.emotion_history
        )

        stable_emotion = emotion_counts.most_common(1)[0][0]

        return stable_emotion


    def reset(self):

        self.emotion_history.clear()


if __name__ == "__main__":

    stabilizer = EmotionStabilizer(
        history_size=7
    )

    test_emotions = [
        "Happy",
        "Happy",
        "Neutral",
        "Happy",
        "Sad",
        "Happy",
        "Neutral"
    ]

    print("\nEmotion Stabilizer Test\n")

    for emotion in test_emotions:

        stable_emotion = stabilizer.update(
            emotion
        )

        print(
            f"Detected: {emotion:8} "
            f"→ Stable: {stable_emotion}"
        )