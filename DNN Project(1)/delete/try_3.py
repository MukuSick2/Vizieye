# import cv2
# import mediapipe as mp
# import numpy as np
# import screen_brightness_control as sbc
# import datetime

# # Initialize MediaPipe Hands
# mp_hands = mp.solutions.hands
# hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7)
# mp_drawing = mp.solutions.drawing_utils

# # Function to adjust brightness
# def adjust_brightness(distance):
#     brightness = max(0, min(100, distance * 100))
#     sbc.set_brightness(brightness)
#     return brightness

# # Function to apply color filter
# def apply_color_filter(image, filter_type):
#     if filter_type == 'RED':
#         return cv2.addWeighted(image, 0.5, np.zeros(image.shape, image.dtype), 0, 0)
#     elif filter_type == 'GREEN':
#         return cv2.addWeighted(image, 0.5, np.zeros(image.shape, image.dtype), 0, 0)
#     elif filter_type == 'BLUE':
#         return cv2.addWeighted(image, 0.5, np.zeros(image.shape, image.dtype), 0, 0)
#     return image

# # Function to take a screenshot
# def take_screenshot(image):
#     timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
#     cv2.imwrite(f"screenshot_{timestamp}.png", image)
#     print(f"Screenshot saved as screenshot_{timestamp}.png")

# # Start video capture
# cap = cv2.VideoCapture(0)
# current_filter = None

# while cap.isOpened():
#     success, image = cap.read()
#     if not success:
#         break

#     image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#     results = hands.process(image_rgb)

#     current_brightness = 0

#     if results.multi_hand_landmarks:
#         for hand_landmarks in results.multi_hand_landmarks:
#             # Draw hand landmarks
#             mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

#             thumb = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
#             index_finger = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
#             middle_finger = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]

#             # Adjust brightness
#             distance = np.linalg.norm(np.array([thumb.x, thumb.y]) - np.array([index_finger.x, index_finger.y]))
#             current_brightness = adjust_brightness(distance)

#             # Detect color filter gesture (e.g., thumb and index finger together for RED, etc.)
#             if index_finger.x < thumb.x and index_finger.y < thumb.y:  # Example gesture for RED
#                 current_filter = 'RED'
#             elif index_finger.x < thumb.x and index_finger.y > thumb.y:  # Example gesture for GREEN
#                 current_filter = 'GREEN'
#             elif middle_finger.x < thumb.x:  # Example gesture for BLUE
#                 current_filter = 'BLUE'
#             elif distance < 0.05:  # Close together to take a screenshot
#                 take_screenshot(image)

#     # Apply color filter if set
#     if current_filter:
#         image = apply_color_filter(image, current_filter)

#     # Display indicators
#     cv2.putText(image, f"Brightness: {current_brightness}%", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
#     cv2.putText(image, f"Filter: {current_filter if current_filter else 'None'}", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

#     # Show the video feed
#     cv2.imshow('Webcam Feed', image)

#     if cv2.waitKey(1) & 0xFF == 27:  # Press 'Esc' to exit
#         break

# cap.release()
# cv2.destroyAllWindows()




import cv2
import mediapipe as mp
import numpy as np
import screen_brightness_control as sbc
import datetime
import tkinter as tk
from tkinter import messagebox
from threading import Thread

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

class BrightnessControlApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Brightness Control with Hand Gestures")
        
        self.start_button = tk.Button(root, text="Start Webcam", command=self.start_webcam)
        self.start_button.pack(pady=20)

        self.stop_button = tk.Button(root, text="Stop Webcam", command=self.stop_webcam, state=tk.DISABLED)
        self.stop_button.pack(pady=20)

        self.status_label = tk.Label(root, text="Status: Not Running")
        self.status_label.pack(pady=20)

        self.current_filter = None
        self.is_running = False

    def start_webcam(self):
        self.is_running = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.status_label.config(text="Status: Running")
        Thread(target=self.run_webcam).start()

    def stop_webcam(self):
        self.is_running = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.status_label.config(text="Status: Not Running")
        
    def adjust_brightness(self, distance):
        brightness = max(0, min(100, distance * 100))
        sbc.set_brightness(brightness)
        return brightness

    def apply_color_filter(self, image, filter_type):
        if filter_type == 'RED':
            image[:, :, 1] = 0  # Remove green channel
            image[:, :, 2] = 0  # Remove blue channel
        elif filter_type == 'GREEN':
            image[:, :, 0] = 0  # Remove red channel
            image[:, :, 2] = 0  # Remove blue channel
        elif filter_type == 'BLUE':
            image[:, :, 0] = 0  # Remove red channel
            image[:, :, 1] = 0  # Remove green channel
        return image

    def take_screenshot(self, image):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        cv2.imwrite(f"screenshot_{timestamp}.png", image)
        messagebox.showinfo("Screenshot", f"Screenshot saved as screenshot_{timestamp}.png")

    def run_webcam(self):
        cap = cv2.VideoCapture(0)
        while self.is_running:
            success, image = cap.read()
            if not success:
                break

            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = hands.process(image_rgb)

            current_brightness = 0

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                    thumb = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
                    index_finger = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                    middle_finger = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]

                    distance = np.linalg.norm(np.array([thumb.x, thumb.y]) - np.array([index_finger.x, index_finger.y]))
                    current_brightness = self.adjust_brightness(distance)

                    if index_finger.x < thumb.x and index_finger.y < thumb.y:  # Example gesture for RED
                        self.current_filter = 'RED'
                    elif index_finger.x < thumb.x and index_finger.y > thumb.y:  # Example gesture for GREEN
                        self.current_filter = 'GREEN'
                    elif middle_finger.x < thumb.x:  # Example gesture for BLUE
                        self.current_filter = 'BLUE'
                    elif distance < 0.05:  # Close together to take a screenshot
                        self.take_screenshot(image)

            if self.current_filter:
                image = self.apply_color_filter(image, self.current_filter)

            cv2.putText(image, f"Brightness: {current_brightness}%", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv2.putText(image, f"Filter: {self.current_filter if self.current_filter else 'None'}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

            cv2.imshow('Webcam Feed', image)

            if cv2.waitKey(1) & 0xFF == 27:  # Press 'Esc' to exit
                break

        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    root = tk.Tk()
    app = BrightnessControlApp(root)
    root.mainloop()