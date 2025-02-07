# import cv2
# import mediapipe as mp
# import numpy as np
# from fastapi import FastAPI, WebSocket
# from fastapi.responses import HTMLResponse
# from typing import Dict


# from fastapi.middleware.cors import CORSMiddleware

# # Initialize FastAPI app
# app = FastAPI()

# # Add CORS middleware
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Allow all origins or specify specific origins
#     allow_credentials=True,
#     allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
#     allow_headers=["*"],  # Allow all headers
# )



# # Functions to initialize MediaPipe models
# def initialize_face_detection():
#     print('model')
#     return mp.solutions.face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5)

# def initialize_face_mesh():
#     print('mesh')
#     return mp.solutions.face_mesh.FaceMesh(max_num_faces=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)

# # Face Detection Function
# def run_face_detection(image: np.ndarray, face_detection) -> Dict:
#     print('rundetected')
#     rgb_frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#     results = face_detection.process(rgb_frame)

#     if results.detections:
#         return {"message": "Face Detected"}
#     else:
#         return {"message": "No Face Detected"}

# # Gaze Tracking Function
# def run_gaze_tracking(image: np.ndarray, face_mesh) -> Dict:
#     print('gaze')
#     rgb_frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#     results = face_mesh.process(rgb_frame)

#     if results.multi_face_landmarks:
#         for face_landmarks in results.multi_face_landmarks:
#             h, w, _ = image.shape
#             left_eye = [face_landmarks.landmark[i] for i in [33, 133, 160, 144, 145, 153]]
#             right_eye = [face_landmarks.landmark[i] for i in [362, 263, 387, 373, 374, 380]]

#             def eye_center(eye):
#                 x = int(np.mean([landmark.x * w for landmark in eye]))
#                 y = int(np.mean([landmark.y * h for landmark in eye]))
#                 return x, y

#             left_eye_center = eye_center(left_eye)
#             right_eye_center = eye_center(right_eye)

#             avg_eye_x = (left_eye_center[0] + right_eye_center[0]) // 2
#             if avg_eye_x < w // 3:
#                 return {"message": "Gaze: Left"}
#             elif avg_eye_x > 2 * w // 3:
#                 return {"message": "Gaze: Right"}
#         return {"message": "Gaze: Straight"}
#     else:
#         return {"message": "No Face for Gaze Tracking"}

# @app.websocket("/ws/process-video")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     face_detection = initialize_face_detection()
#     face_mesh = initialize_face_mesh()
#     print('ws')
#     try:
#         while True:
#             # Receive binary frame data
#             data = await websocket.receive_bytes()
#             print('here')
#             nparr = np.frombuffer(data, np.uint8)
#             frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

#             # Run detection and tracking
#             face_result = run_face_detection(frame, face_detection)
#             gaze_result = run_gaze_tracking(frame, face_mesh)

#             # Send results back to the client
#             await websocket.send_json({
#                 "face_detection": face_result,
#                 "gaze_tracking": gaze_result
#             })
#             print("sent reply")

#     except Exception as e:
#         print("except")
#         await websocket.close()
#         print(f"WebSocket connection closed: {e}")

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run("main:app", port=8001, reload=True)



import cv2
import mediapipe as mp
import numpy as np
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from typing import Dict
from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI app
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins or specify specific origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Initialize MediaPipe models
def initialize_face_detection():
    return mp.solutions.face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5)

def initialize_face_mesh():
    return mp.solutions.face_mesh.FaceMesh(max_num_faces=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Face Detection Function
def run_face_detection(image: np.ndarray, face_detection) -> Dict:
    rgb_frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = face_detection.process(rgb_frame)

    if results.detections:
        return {"message": "Face Detected"}
    else:
        return {"message": "No Face Detected"}

# Gaze Tracking Function with angle calculation
def run_gaze_tracking(image: np.ndarray, face_mesh) -> Dict:
    rgb_frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_frame)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            h, w, _ = image.shape
            left_eye = [face_landmarks.landmark[i] for i in [33, 133, 160, 144, 145, 153]]
            right_eye = [face_landmarks.landmark[i] for i in [362, 263, 387, 373, 374, 380]]

            def eye_center(eye):
                x = int(np.mean([landmark.x * w for landmark in eye]))
                y = int(np.mean([landmark.y * h for landmark in eye]))
                return x, y

            left_eye_center = eye_center(left_eye)
            right_eye_center = eye_center(right_eye)

            # Calculate the distance and angle between eyes to determine gaze direction
            dx = right_eye_center[0] - left_eye_center[0]
            dy = right_eye_center[1] - left_eye_center[1]
            angle = np.arctan2(dy, dx) * 180 / np.pi  # Convert to degrees

            print(f"Angle: {angle}")

            # If the angle is outside of a threshold, consider the gaze as left or right
            if angle < -7:  # Gaze to the left
                return {"message": "Gaze: Left"}
            elif angle > 7:  # Gaze to the right
                return {"message": "Gaze: Right"}
            else:  # Straight gaze
                return {"message": "Gaze: Straight"}

    return {"message": "No Face for Gaze Tracking"}

@app.websocket("/ws/process-video")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    face_detection = initialize_face_detection()
    face_mesh = initialize_face_mesh()

    try:
        while True:
            data = await websocket.receive_bytes()
            nparr = np.frombuffer(data, np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            # Run detection and tracking
            face_result = run_face_detection(frame, face_detection)
            gaze_result = run_gaze_tracking(frame, face_mesh)

            # Send results back to the client
            await websocket.send_json({
                "face_detection": face_result,
                "gaze_tracking": gaze_result
            })

    except Exception as e:
        await websocket.close()
        print(f"WebSocket connection closed: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", port=8001, reload=True)








