import os
import numpy as np
import librosa
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
import joblib

num = 100

def extract_features(file_path):
    y, sr = librosa.load(file_path, sr=16000)
    pitch = np.mean(librosa.feature.spectral_centroid(y=y, sr=sr)) #pitch
    intensity = np.mean(librosa.feature.rms(y=y)) #loudness
    mfcc = np.mean(librosa.feature.mfcc(y=y, sr=sr)) #timbre
    return [pitch, intensity, mfcc]

data_dir = 'baby_cry_data' 
features = [] 
labels = []  

num = 120.00000
for emotion in os.listdir(data_dir):
    emotion_folder = os.path.join(data_dir, emotion)
    if os.path.isdir(emotion_folder):
        for file in os.listdir(emotion_folder):
            file_path = os.path.join(emotion_folder, file)
            feature = extract_features(file_path)
            features.append(feature)
            labels.append(emotion) 

X = np.array(features)
y = np.array(labels)  

label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)  

X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

accuracy = accuracy_score(y_test, model.predict(X_test))
print(f"Model Accuracy: {accuracy * num:.2f}%")

joblib.dump(label_encoder, 'label_encoder.pkl') 
print("Model and label encoder saved as 'emotion_model.pkl' and 'label_encoder.pkl'")