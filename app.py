import cv2
import customtkinter as ctk
from PIL import Image, ImageTk

from face_detection.face_detector import FaceDetector
from emotion_detection.emotion_detector import EmotionDetector
from emotion_detection.emotion_stabilizer import EmotionStabilizer
from emotion_detection.mood_confirmation import MoodConfirmation


# ============================================================
# CUSTOMTKINTER SETTINGS
# ============================================================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


# ============================================================
# MOODSYNC AI APPLICATION
# ============================================================

class MoodSyncApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        # ----------------------------------------------------
        # WINDOW
        # ----------------------------------------------------

        self.title("MoodSync AI")
        self.geometry("1200x750")
        self.minsize(1000, 650)

        # ----------------------------------------------------
        # CAMERA VARIABLES
        # ----------------------------------------------------

        self.camera = None
        self.camera_running = False

        # Dedicated reference for Tkinter PhotoImage
        self.current_photo = None

        # ----------------------------------------------------
        # AI COMPONENTS
        # ----------------------------------------------------

        print("Initializing Face Detector...")

        self.face_detector = FaceDetector()

        print("Initializing Emotion Detector...")

        self.emotion_detector = EmotionDetector()

        print("Initializing Emotion Stabilizer...")

        self.emotion_stabilizer = EmotionStabilizer(
            history_size=7
        )

        print("Initializing Mood Confirmation...")

        self.mood_confirmation = MoodConfirmation(
            required_count=5
        )

        print("MoodSync AI components initialized!")

        # ----------------------------------------------------
        # GRID CONFIGURATION
        # ----------------------------------------------------

        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=2)

        self.grid_rowconfigure(1, weight=1)

        # ----------------------------------------------------
        # HEADER
        # ----------------------------------------------------

        self.header_frame = ctk.CTkFrame(
            self,
            corner_radius=15
        )

        self.header_frame.grid(
            row=0,
            column=0,
            columnspan=2,
            padx=20,
            pady=(20, 10),
            sticky="ew"
        )

        self.header_frame.grid_columnconfigure(
            0,
            weight=1
        )

        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text="🎧 MoodSync AI",
            font=ctk.CTkFont(
                size=28,
                weight="bold"
            )
        )

        self.title_label.grid(
            row=0,
            column=0,
            padx=20,
            pady=(15, 2),
            sticky="w"
        )

        self.subtitle_label = ctk.CTkLabel(
            self.header_frame,
            text="Emotion-Aware Music Recommendation System",
            font=ctk.CTkFont(
                size=14
            )
        )

        self.subtitle_label.grid(
            row=1,
            column=0,
            padx=20,
            pady=(0, 15),
            sticky="w"
        )

        # ----------------------------------------------------
        # CAMERA FRAME
        # ----------------------------------------------------

        self.camera_frame = ctk.CTkFrame(
            self,
            corner_radius=15
        )

        self.camera_frame.grid(
            row=1,
            column=0,
            padx=(20, 10),
            pady=10,
            sticky="nsew"
        )

        self.camera_frame.grid_rowconfigure(
            1,
            weight=1
        )

        self.camera_frame.grid_columnconfigure(
            0,
            weight=1
        )

        self.camera_title = ctk.CTkLabel(
            self.camera_frame,
            text="📷 Live Camera",
            font=ctk.CTkFont(
                size=20,
                weight="bold"
            )
        )

        self.camera_title.grid(
            row=0,
            column=0,
            padx=15,
            pady=15,
            sticky="w"
        )

        self.camera_label = ctk.CTkLabel(
            self.camera_frame,
            text="Camera is off",
            font=ctk.CTkFont(
                size=18
            ),
            corner_radius=10
        )

        self.camera_label.grid(
            row=1,
            column=0,
            padx=15,
            pady=(0, 15),
            sticky="nsew"
        )

        # ----------------------------------------------------
        # RIGHT PANEL
        # ----------------------------------------------------

        self.right_frame = ctk.CTkFrame(
            self,
            corner_radius=15
        )

        self.right_frame.grid(
            row=1,
            column=1,
            padx=(10, 20),
            pady=10,
            sticky="nsew"
        )

        # ----------------------------------------------------
        # SYSTEM STATUS
        # ----------------------------------------------------

        self.status_title = ctk.CTkLabel(
            self.right_frame,
            text="System Status",
            font=ctk.CTkFont(
                size=18,
                weight="bold"
            )
        )

        self.status_title.pack(
            padx=20,
            pady=(20, 5)
        )

        self.status_label = ctk.CTkLabel(
            self.right_frame,
            text="●  SYSTEM READY",
            font=ctk.CTkFont(
                size=15
            )
        )

        self.status_label.pack(
            padx=20,
            pady=(0, 20)
        )

        # ----------------------------------------------------
        # CONFIRMED MOOD
        # ----------------------------------------------------

        self.mood_title = ctk.CTkLabel(
            self.right_frame,
            text="Confirmed Mood",
            font=ctk.CTkFont(
                size=18,
                weight="bold"
            )
        )

        self.mood_title.pack(
            padx=20,
            pady=(10, 5)
        )

        self.mood_label = ctk.CTkLabel(
            self.right_frame,
            text="😊 Waiting...",
            font=ctk.CTkFont(
                size=30,
                weight="bold"
            )
        )

        self.mood_label.pack(
            padx=20,
            pady=(5, 20)
        )

        # ----------------------------------------------------
        # RAW EMOTION
        # ----------------------------------------------------

        self.raw_emotion_label = ctk.CTkLabel(
            self.right_frame,
            text="Raw Emotion: Waiting...",
            font=ctk.CTkFont(
                size=14
            )
        )

        self.raw_emotion_label.pack(
            padx=20,
            pady=(0, 15)
        )

        # ----------------------------------------------------
        # CONFIDENCE
        # ----------------------------------------------------

        self.confidence_title = ctk.CTkLabel(
            self.right_frame,
            text="Emotion Confidence",
            font=ctk.CTkFont(
                size=18,
                weight="bold"
            )
        )

        self.confidence_title.pack(
            padx=20,
            pady=(5, 5)
        )

        self.confidence_label = ctk.CTkLabel(
            self.right_frame,
            text="0%",
            font=ctk.CTkFont(
                size=20
            )
        )

        self.confidence_label.pack(
            padx=20,
            pady=(0, 8)
        )

        self.confidence_bar = ctk.CTkProgressBar(
            self.right_frame,
            width=250
        )

        self.confidence_bar.pack(
            padx=20,
            pady=(0, 25)
        )

        self.confidence_bar.set(0)

        # ----------------------------------------------------
        # MOOD CONFIRMATION
        # ----------------------------------------------------

        self.confirmation_label = ctk.CTkLabel(
            self.right_frame,
            text="Mood Confirmation: Waiting...",
            font=ctk.CTkFont(
                size=13
            )
        )

        self.confirmation_label.pack(
            padx=20,
            pady=(0, 20)
        )

        # ----------------------------------------------------
        # YOUTUBE
        # ----------------------------------------------------

        self.youtube_title = ctk.CTkLabel(
            self.right_frame,
            text="▶ YouTube Recommendation",
            font=ctk.CTkFont(
                size=18,
                weight="bold"
            )
        )

        self.youtube_title.pack(
            padx=20,
            pady=(5, 5)
        )

        self.youtube_label = ctk.CTkLabel(
            self.right_frame,
            text="Waiting for confirmed mood...",
            font=ctk.CTkFont(
                size=14
            ),
            wraplength=300
        )

        self.youtube_label.pack(
            padx=20,
            pady=(0, 20)
        )

        # ----------------------------------------------------
        # CONTROLS
        # ----------------------------------------------------

        self.controls_frame = ctk.CTkFrame(
            self.right_frame,
            fg_color="transparent"
        )

        self.controls_frame.pack(
            padx=20,
            pady=(10, 20),
            fill="x"
        )

        self.controls_frame.grid_columnconfigure(
            0,
            weight=1
        )

        self.controls_frame.grid_columnconfigure(
            1,
            weight=1
        )

        self.start_button = ctk.CTkButton(
            self.controls_frame,
            text="▶ START",
            height=45,
            font=ctk.CTkFont(
                size=15,
                weight="bold"
            ),
            command=self.start_camera
        )

        self.start_button.grid(
            row=0,
            column=0,
            padx=(0, 5),
            sticky="ew"
        )

        self.stop_button = ctk.CTkButton(
            self.controls_frame,
            text="■ STOP",
            height=45,
            font=ctk.CTkFont(
                size=15,
                weight="bold"
            ),
            command=self.stop_camera
        )

        self.stop_button.grid(
            row=0,
            column=1,
            padx=(5, 0),
            sticky="ew"
        )

        # ----------------------------------------------------
        # CLOSE EVENT
        # ----------------------------------------------------

        self.protocol(
            "WM_DELETE_WINDOW",
            self.close_app
        )

    # ========================================================
    # START CAMERA
    # ========================================================

    def start_camera(self):

        if self.camera_running:
            return

        print("\nStarting camera...")

        # Reset AI pipeline
        self.emotion_stabilizer.reset()
        self.mood_confirmation.reset()

        self.camera = cv2.VideoCapture(0)

        if not self.camera.isOpened():

            print("❌ Could not open camera.")

            self.status_label.configure(
                text="●  CAMERA ERROR"
            )

            self.camera = None

            return

        self.camera_running = True

        self.status_label.configure(
            text="●  CAMERA ACTIVE"
        )

        self.mood_label.configure(
            text="😊 Detecting..."
        )

        self.raw_emotion_label.configure(
            text="Raw Emotion: Waiting..."
        )

        self.confidence_label.configure(
            text="0%"
        )

        self.confidence_bar.set(0)

        self.confirmation_label.configure(
            text="Mood Confirmation: Detecting..."
        )

        self.youtube_label.configure(
            text="Waiting for confirmed mood..."
        )

        print("✅ Camera started.")

        self.update_camera()

    # ========================================================
    # UPDATE CAMERA
    # ========================================================

    def update_camera(self):

        # Important:
        # Do not process another frame after STOP.
        if not self.camera_running:
            return

        # Safety check
        if self.camera is None:
            return

        ret, frame = self.camera.read()

        if not ret:

            print("❌ Failed to read camera frame.")

            self.status_label.configure(
                text="●  CAMERA ERROR"
            )

            self.stop_camera()

            return

        # ----------------------------------------------------
        # MIRROR CAMERA
        # ----------------------------------------------------

        frame = cv2.flip(
            frame,
            1
        )

        # ----------------------------------------------------
        # FACE DETECTION
        # ----------------------------------------------------

        faces = self.face_detector.detect_faces(
            frame
        )

        detected_emotion = None
        detected_confidence = 0.0

        # ----------------------------------------------------
        # FACE FOUND
        # ----------------------------------------------------

        if len(faces) > 0:

            # Select largest face
            largest_face = max(
                faces,
                key=lambda face: face[2] * face[3]
            )

            x, y, w, h = largest_face

            # ------------------------------------------------
            # CROP FACE
            # ------------------------------------------------

            face_crop = frame[
                y:y + h,
                x:x + w
            ]

            # ------------------------------------------------
            # EMOTION DETECTION
            # ------------------------------------------------

            if face_crop.size > 0:

                try:

                    (
                        detected_emotion,
                        detected_confidence
                    ) = self.emotion_detector.predict_emotion(
                        face_crop
                    )

                except Exception as error:

                    print(
                        f"Emotion detection error: {error}"
                    )

                    detected_emotion = None
                    detected_confidence = 0.0

            # ------------------------------------------------
            # DRAW ALL FACE BOXES
            # ------------------------------------------------

            for (
                face_x,
                face_y,
                face_w,
                face_h
            ) in faces:

                cv2.rectangle(
                    frame,
                    (
                        face_x,
                        face_y
                    ),
                    (
                        face_x + face_w,
                        face_y + face_h
                    ),
                    (0, 255, 0),
                    2
                )

            # ------------------------------------------------
            # EMOTION STABILIZATION
            # ------------------------------------------------

            stable_emotion = None

            if detected_emotion:

                stable_emotion = (
                    self.emotion_stabilizer.update(
                        detected_emotion
                    )
                )

            # ------------------------------------------------
            # MOOD CONFIRMATION
            # ------------------------------------------------

            confirmed_mood = (
                self.mood_confirmation.update(
                    stable_emotion
                )
            )

            # ------------------------------------------------
            # CAMERA EMOTION TEXT
            # ------------------------------------------------

            if detected_emotion:

                emotion_text = (
                    f"{detected_emotion} "
                    f"{detected_confidence * 100:.1f}%"
                )

                text_y = y - 10

                if text_y < 30:

                    text_y = (
                        y + h + 30
                    )

                cv2.putText(
                    frame,
                    emotion_text,
                    (
                        x,
                        text_y
                    ),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 255, 0),
                    2,
                    cv2.LINE_AA
                )

            # ------------------------------------------------
            # UPDATE RAW EMOTION
            # ------------------------------------------------

            if detected_emotion:

                self.raw_emotion_label.configure(
                    text=(
                        f"Raw Emotion: "
                        f"{detected_emotion}"
                    )
                )

                confidence_percentage = (
                    detected_confidence * 100
                )

                self.confidence_label.configure(
                    text=(
                        f"{confidence_percentage:.1f}%"
                    )
                )

                self.confidence_bar.set(
                    min(
                        detected_confidence,
                        1.0
                    )
                )

            # ------------------------------------------------
            # UPDATE CONFIRMED MOOD
            # ------------------------------------------------

            if confirmed_mood:

                emoji = self.get_emotion_emoji(
                    confirmed_mood
                )

                self.mood_label.configure(
                    text=(
                        f"{emoji} "
                        f"{confirmed_mood}"
                    )
                )

                self.confirmation_label.configure(
                    text="✓ Mood Confirmed"
                )

            elif stable_emotion:

                self.confirmation_label.configure(
                    text=(
                        f"Stabilizing: "
                        f"{stable_emotion}"
                    )
                )

        # ----------------------------------------------------
        # NO FACE DETECTED
        # ----------------------------------------------------

        else:

            self.mood_label.configure(
                text="😊 No Face"
            )

            self.raw_emotion_label.configure(
                text="Raw Emotion: Waiting..."
            )

            self.confidence_label.configure(
                text="0%"
            )

            self.confidence_bar.set(0)

            self.confirmation_label.configure(
                text="Mood Confirmation: Waiting..."
            )

        # ----------------------------------------------------
        # BGR → RGB
        # ----------------------------------------------------

        frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        # ----------------------------------------------------
        # RESIZE CAMERA FRAME
        # ----------------------------------------------------

        width = self.camera_label.winfo_width()
        height = self.camera_label.winfo_height()

        if width > 10 and height > 10:

            frame = cv2.resize(
                frame,
                (
                    width,
                    height
                )
            )

        # ----------------------------------------------------
        # CREATE PIL IMAGE
        # ----------------------------------------------------

        image = Image.fromarray(
            frame
        )

        # ----------------------------------------------------
        # CREATE TKINTER IMAGE
        # ----------------------------------------------------

        photo = ImageTk.PhotoImage(
            image=image
        )

        # Keep a strong reference.
        # This prevents:
        # _tkinter.TclError:
        # image "pyimageXXX" doesn't exist

        self.current_photo = photo

        # ----------------------------------------------------
        # DISPLAY IMAGE
        # ----------------------------------------------------

        self.camera_label.configure(
            image=self.current_photo,
            text=""
        )

        # ----------------------------------------------------
        # SCHEDULE NEXT FRAME
        # ----------------------------------------------------

        if self.camera_running:

            self.after(
                30,
                self.update_camera
            )

    # ========================================================
    # EMOTION EMOJI
    # ========================================================

    def get_emotion_emoji(
        self,
        emotion
    ):

        emotion_emojis = {

            "Angry": "😠",

            "Disgust": "🤢",

            "Fear": "😨",

            "Happy": "😊",

            "Neutral": "😐",

            "Sad": "😢",

            "Surprise": "😲"

        }

        return emotion_emojis.get(
            emotion,
            "🙂"
        )

    # ========================================================
    # STOP CAMERA
    # ========================================================

    def stop_camera(self):

        # ----------------------------------------------------
        # FIRST STOP FUTURE CALLBACKS
        # ----------------------------------------------------

        self.camera_running = False

        # ----------------------------------------------------
        # RELEASE CAMERA
        # ----------------------------------------------------

        if self.camera is not None:

            self.camera.release()

            self.camera = None

        # ----------------------------------------------------
        # RESET AI
        # ----------------------------------------------------

        self.emotion_stabilizer.reset()

        self.mood_confirmation.reset()

        # ----------------------------------------------------
        # CLEAR CAMERA IMAGE SAFELY
        # ----------------------------------------------------

        self.current_photo = None

        self.camera_label.configure(
            image=None,
            text="Camera is off"
        )

        # ----------------------------------------------------
        # RESET UI
        # ----------------------------------------------------

        self.status_label.configure(
            text="●  SYSTEM READY"
        )

        self.mood_label.configure(
            text="😊 Waiting..."
        )

        self.raw_emotion_label.configure(
            text="Raw Emotion: Waiting..."
        )

        self.confidence_label.configure(
            text="0%"
        )

        self.confidence_bar.set(0)

        self.confirmation_label.configure(
            text="Mood Confirmation: Waiting..."
        )

        self.youtube_label.configure(
            text="Waiting for confirmed mood..."
        )

        print("Camera stopped.")

    # ========================================================
    # CLOSE APPLICATION
    # ========================================================

    def close_app(self):

        print("Closing MoodSync AI...")

        self.stop_camera()

        self.destroy()


# ============================================================
# APPLICATION START
# ============================================================

if __name__ == "__main__":

    app = MoodSyncApp()

    app.mainloop()