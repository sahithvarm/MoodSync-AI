class MoodConfirmation:

    def __init__(self, required_count=5):

        self.required_count = required_count

        self.current_mood = None
        self.candidate_mood = None
        self.candidate_count = 0


    def update(self, mood):

        if not mood:
            return self.current_mood


        # First mood detected
        if self.current_mood is None:

            self.current_mood = mood

            return self.current_mood


        # Same as current mood
        if mood == self.current_mood:

            self.candidate_mood = None
            self.candidate_count = 0

            return self.current_mood


        # New candidate mood
        if mood == self.candidate_mood:

            self.candidate_count += 1

        else:

            self.candidate_mood = mood
            self.candidate_count = 1


        # Confirm the new mood
        if self.candidate_count >= self.required_count:

            self.current_mood = self.candidate_mood

            self.candidate_mood = None
            self.candidate_count = 0


        return self.current_mood


    def reset(self):

        self.current_mood = None
        self.candidate_mood = None
        self.candidate_count = 0


if __name__ == "__main__":

    confirmation = MoodConfirmation(
        required_count=5
    )


    test_moods = [

        "happy",
        "happy",
        "happy",

        "sad",
        "sad",
        "sad",
        "sad",

        "happy",
        "happy",
        "happy",
        "happy",
        "happy"
    ]


    print("\nMood Confirmation Test\n")


    for mood in test_moods:

        confirmed_mood = confirmation.update(
            mood
        )

        print(
            f"Detected: {mood:8} "
            f"→ Confirmed: {confirmed_mood}"
        )
