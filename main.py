import cv2

from face_detection.face_detector import FaceDetector
from emotion_detection.emotion_detector import EmotionDetector
from emotion_detection.emotion_stabilizer import EmotionStabilizer
from emotion_detection.mood_confirmation import MoodConfirmation
from music.mood_mapper import MoodMapper
from youtube.youtube_mood_controller import YouTubeMoodController


# ============================================================
# YOUTUBE API KEY
# ============================================================

API_KEY = "AIzaSyBljiPMNaU4CTdFqgLmfXcEnP06jwLoVGU"


# ============================================================
# CAMERA SETUP
# ============================================================

camera = cv2.VideoCapture(0)

if not camera.isOpened():

    print(
        "Error: Could not open camera."
    )

    exit()


# ============================================================
# INITIALIZE COMPONENTS
# ============================================================

face_detector = FaceDetector()

emotion_detector = EmotionDetector()

emotion_stabilizer = EmotionStabilizer(
    history_size=7
)

mood_confirmation = MoodConfirmation(
    required_count=5
)

mood_mapper = MoodMapper()

youtube_controller = YouTubeMoodController(
    API_KEY,
    cooldown_seconds=60
)


# ============================================================
# SETTINGS
# ============================================================

MIN_CONFIDENCE = 0.60


# ============================================================
# MAIN LOOP
# ============================================================

while True:

    ret, frame = camera.read()


    if not ret:

        print(
            "Error: Could not read camera frame."
        )

        break


    # ========================================================
    # CAMERA ORIENTATION
    # ========================================================

    frame = cv2.flip(
        frame,
        1
    )


    # ========================================================
    # FACE DETECTION
    # ========================================================

    faces = face_detector.detect_faces(
        frame
    )


    for (x, y, w, h) in faces:

        face = frame[
            y:y + h,
            x:x + w
        ]


        # ====================================================
        # EMOTION DETECTION
        # ====================================================

        emotion, confidence = (
            emotion_detector.predict_emotion(
                face
            )
        )


        # ====================================================
        # CONFIDENCE FILTER
        # ====================================================

        if confidence >= MIN_CONFIDENCE:


            # =================================================
            # EMOTION STABILIZATION
            # =================================================

            stable_emotion = (
                emotion_stabilizer.update(
                    emotion
                )
            )


            # =================================================
            # MOOD MAPPING
            # =================================================

            detected_mood = (
                mood_mapper.get_music_mood(
                    stable_emotion
                )
            )


            # =================================================
            # MOOD CONFIRMATION
            # =================================================

            confirmed_mood = (
                mood_confirmation.update(
                    detected_mood
                )
            )


            # =================================================
            # YOUTUBE
            # =================================================

            youtube_controller.handle_mood(
                confirmed_mood
            )


            # =================================================
            # DISPLAY
            # =================================================

            emotion_text = (
                f"{stable_emotion} "
                f"({confidence * 100:.1f}%)"
            )


            mood_text = (
                f"YouTube: "
                f"{confirmed_mood}"
            )


        else:

            # =================================================
            # LOW CONFIDENCE
            # =================================================

            emotion_text = (
                f"Uncertain "
                f"({confidence * 100:.1f}%)"
            )


            mood_text = (
                "YouTube: Waiting..."
            )


        # ====================================================
        # FACE BOX
        # ====================================================

        cv2.rectangle(
            frame,
            (x, y),
            (x + w, y + h),
            (0, 255, 0),
            2
        )


        # ====================================================
        # EMOTION TEXT
        # ====================================================

        cv2.putText(
            frame,
            emotion_text,
            (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )


        # ====================================================
        # YOUTUBE MOOD TEXT
        # ====================================================

        cv2.putText(
            frame,
            mood_text,
            (x, y + h + 25),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 0),
            2
        )


    # ========================================================
    # DISPLAY CAMERA
    # ========================================================

    cv2.imshow(
        "MoodSync AI",
        frame
    )


    # ========================================================
    # QUIT
    # ========================================================

    if cv2.waitKey(1) & 0xFF == ord("q"):

        break


# ============================================================
# CLEANUP
# ============================================================

camera.release()

cv2.destroyAllWindows()
