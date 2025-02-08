import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np
import cv2



def spiral_in_pattern(rows, cols):
    top, bottom, left, right = 0, rows - 1, 0, cols - 1
    direction = 0  # 0: right, 1: down, 2: left, 3: up
    spiral = []

    while top <= bottom and left <= right:
        if direction == 0:
            for i in range(left, right + 1):
                spiral.append((top, i))
            top += 1
        elif direction == 1:
            for i in range(top, bottom + 1):
                spiral.append((i, right))
            right -= 1
        elif direction == 2:
            for i in range(right, left - 1, -1):
                spiral.append((bottom, i))
            bottom -= 1
        elif direction == 3:
            for i in range(bottom, top - 1, -1):
                spiral.append((i, left))
            left += 1
        direction = (direction + 1) % 4

    return spiral

def encrypt_image(image_path):
    image = cv2.imread(image_path)
    if image is None:
        print("Image not found.")
        return

    rows, cols, _ = image.shape
    spiral_order = spiral_in_pattern(rows, cols)

    encrypted_image = np.zeros_like(image)

    for i, (row, col) in enumerate(spiral_order):
        encrypted_image[row, col] = image[i // cols, i % cols]

    cv2.imwrite("Spiral_IN.png", encrypted_image)
    print("Image encrypted and saved as 'Spiral_IN.png'.")

class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Image Encryption Tool")
        self.geometry("600x400")

        self.image_label = tk.Label(self, text="Select an image to encrypt:")
        self.image_label.pack(pady=10)

        self.encrypt_button = tk.Button(self, text="Encrypt Image", command=self.encrypt_image)
        self.encrypt_button.pack(pady=5)

        self.show_encrypted_button = tk.Button(self, text="Show Encrypted Image", command=self.show_encrypted_image)
        self.show_encrypted_button.pack(pady=5)

    def encrypt_image(self):
        file_path = filedialog.askopenfilename(title="Select Image", filetypes=(("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")))
        if file_path:
            encrypt_image(file_path)

    def show_encrypted_image(self):
        file_path = "Spiral_IN.png"
        if file_path:
            encrypted_image = Image.open(file_path)
            encrypted_image.show()

if __name__ == "__main__":
    app = Application()
    app.mainloop()
