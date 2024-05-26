import numpy as np
import cv2
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D
import os
from pathlib import Path
import time
from tkinter import Tk
from musicplayer import MusicPlayer  # Ensure this module exists
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Suppress TensorFlow logging

# Music player function
def music_player(emotion_str):
    root = Tk()
    print(f'\nPlaying {emotion_str} songs')
    MusicPlayer(root, emotion_str)
    root.mainloop()

# Create the emotion detection model
def create_model():
    model = Sequential([
        Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(48, 48, 1)),
        Conv2D(64, kernel_size=(3, 3), activation='relu'),
        MaxPooling2D(pool_size=(2, 2)),
        Dropout(0.25),
        Conv2D(128, kernel_size=(3, 3), activation='relu'),
        MaxPooling2D(pool_size=(2, 2)),
        Conv2D(128, kernel_size=(3, 3), activation='relu'),
        MaxPooling2D(pool_size=(2, 2)),
        Dropout(0.25),
        Flatten(),
        Dense(1024, activation='relu'),
        Dropout(0.5),
        Dense(7, activation='softmax')
    ])
    return model

# Load the pre-trained model weights
def load_model_weights(model, weights_path='Tensorflow/model.h5'):
    if not os.path.exists(weights_path):
        raise FileNotFoundError(f"Model weights file not found: {weights_path}")
    model.load_weights(weights_path)
    return model

# Main function to start the emotion detection and music player
def main():
    model = create_model()
    model = load_model_weights(model)

    print('\nWelcome to the Music Player based on Facial Emotion Recognition\n')
    print('\nPress \'q\' to exit the music player\n')

    cv2.ocl.setUseOpenCL(False)
    emotion_dict = {0: "Angry", 1: "Disgusted", 2: "Fearful", 3: "Happy", 4: "Neutral", 5: "Sad", 6: "Surprised"}

    haar_cascade_path = 'Tensorflow/haarcascade_frontalface_default.xml'
    if not os.path.exists(haar_cascade_path):
        raise FileNotFoundError(f"Haar Cascade file not found: {haar_cascade_path}")

    try:
        with open(Path.cwd() / "emotion.txt", "w") as emotion_file:
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                print("Error: Could not open webcam.")
                return

            future = time.time() + 10
            while True:
                ret, frame = cap.read()
                if not ret:
                    print("Error: Failed to capture image.")
                    break

                facecasc = cv2.CascadeClassifier(haar_cascade_path)
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = facecasc.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y-50), (x+w, y+h+10), (255, 0, 0), 2)
                    roi_gray = gray[y:y + h, x:x + w]
                    cropped_img = np.expand_dims(np.expand_dims(cv2.resize(roi_gray, (48, 48)), -1), 0)
                    prediction = model.predict(cropped_img)
                    maxindex = int(np.argmax(prediction))
                    emotion = emotion_dict[maxindex]
                    cv2.putText(frame, emotion, (x+20, y-60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
                    emotion_file.write(emotion + "\n")
                    emotion_file.flush()

                cv2.imshow('Video', cv2.resize(frame, (1600, 960), interpolation=cv2.INTER_CUBIC))
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

                if time.time() > future:
                    cv2.destroyAllWindows()
                    music_player(emotion)
                    future = time.time() + 10

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
