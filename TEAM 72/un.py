import tkinter as tk
from tkinter import filedialog, messagebox, PhotoImage
from PIL import Image, ImageTk
import numpy as np
import os
import cv2

root = tk.Tk()
root.title("Image Encryption & Decryption App")
root.geometry("700x400")

button_x = 15
button_y = 100

# Define global variables
original_image = None
encrypted_image = None
cipher_image = None
decrypted_image = None
decrypted_image1=None


label = tk.Label(root)
label.place(x=50,y=130)

image_status_label = tk.Label(root, font=("Helvetica", 20,"italic"))
image_status_label.place(x=160, y=650)
# Function to browse and display the selected image
def browse_image():
    global original_image
    file_path = filedialog.askopenfilename(title="Select Image", filetypes=[("Image Files", "*.png *.jpg *.jpeg")])
    if file_path:
        original_image = Image.open(file_path)
        original_image.thumbnail((500, 300))  # Resize image to fit the canvas
        original_image = original_image.resize((512, 512))  # Custom size: (width, height)

        photo = ImageTk.PhotoImage(original_image)  # Convert image to PhotoImage
        label.config(image=photo)  # Update the label with the new image
        label.image = photo  # Keep a reference to the image to prevent it from being garbage collected
        image_status_label.config(text="Original Image")
def set_active_button(button):
    global active_button
    if active_button:
        active_button.config(bg="SystemButtonFace")  # Reset previous active button color
    active_button = button
    active_button.config(bg="sky blue")  # Set new active button color


# Create buttons for image operations
browse_button = tk.Button(root, text="Browse Image", command=lambda: (set_active_button(browse_button), browse_image()), width=20, height=2,font=("Helvetica", 8,"bold"))
browse_button.place(x=button_x+800, y=button_y+50)

root.mainloop()