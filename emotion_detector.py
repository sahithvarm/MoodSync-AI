import os
import cv2
import numpy as np
import tensorflow as tf


class EmotionDetector:

    def __init__(self):

        model_path = os.path.join(
            os.path.dirname(__file__),
            "models",
            "emotion_model.keras"
        )

        if not os.path.exists(model_path):
            raise FileNotFoundError(
                f"Emotion model not found: {model_path}"
            )

        print("Loading emotion model...")

        self.model = tf.keras.models.load_model(
            model_path,
            compile=False
        )

        print("Emotion model loaded successfully!")
        print("Input shape:", self.model.input_shape)
        print("Output shape:", self.model.output_shape)

        self.emotions = [
            "Angry",
            "Disgust",
            "Fear",
            "Happy",
            "Neutral",
            "Sad",
            "Surprise"
        ]

    def predict_emotion(self, face):

        # Convert face to grayscale
        gray_face = cv2.cvtColor(
            face,
            cv2.COLOR_BGR2GRAY
        )

        # Resize to model input size
        gray_face = cv2.resize(
            gray_face,
            (48, 48)
        )

        # Normalize pixel values
        gray_face = gray_face.astype("float32") / 255.0

        # Add dimensions:
        # (48, 48)
        #     ↓
        # (1, 48, 48, 1)
        input_face = np.expand_dims(
            gray_face,
            axis=-1
        )

        input_face = np.expand_dims(
            input_face,
            axis=0
        )

        # Predict emotion
        predictions = self.model.predict(
            input_face,
            verbose=0
        )[0]

        # Find highest probability
        emotion_index = np.argmax(predictions)

        emotion = self.emotions[emotion_index]

        confidence = float(
            predictions[emotion_index]
        )

        return emotion, confidence