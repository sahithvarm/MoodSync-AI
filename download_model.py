from huggingface_hub import hf_hub_download
import shutil
import os

repo_id = "lokeshkumar79/facial-emotion-recognition"
filename = "finalfacialemotionmodel.keras"

model_path = hf_hub_download(
    repo_id=repo_id,
    filename=filename
)

destination = os.path.join(
    "emotion_detection",
    "models",
    "emotion_model.keras"
)

shutil.copy2(model_path, destination)

print("Emotion model downloaded successfully!")
print(f"Saved to: {destination}")