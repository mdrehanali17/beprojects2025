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

# Create a label to display the background image
bg_img = PhotoImage(file=r"C:\Users\vins2\OneDrive\Desktop\Group 10\Group 10\images1.png")
bg_label = tk.Label(root, image=bg_img)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Create a label to display the images
label = tk.Label(root)
label.place(x=50,y=175)

image_status_label = tk.Label(root, font=("Helvetica", 20,"italic"))
image_status_label.place(x=160, y=650)
# Function to browse and display the selected image
def browse_image():
    global original_image
    file_path = filedialog.askopenfilename(title="Select Image", filetypes=[("Image Files", "*.png *.jpg *.jpeg")])
    if file_path:
        original_image = Image.open(file_path)
        original_image.thumbnail((500, 300))  # Resize image to fit the canvas
        original_image = original_image.resize((256, 256))  # Custom size: (width, height)

        photo = ImageTk.PhotoImage(original_image)  # Convert image to PhotoImage
        label.config(image=photo)  # Update the label with the new image
        label.image = photo  # Keep a reference to the image to prevent it from being garbage collected
        image_status_label.config(text="Original Image")

# Function to perform Zeta-Z pattern operation and display the encrypted image
def zeta_z_operation():
    global original_image, encrypted_image
    if original_image:
        # Get image size
        width, height = original_image.size

        # Get pixels of the original image
        pixels = list(original_image.getdata())

        # Define the Zeta-Z scan pattern
        def zeta_z_scan(width, height):
            scan_pattern = []
            for d in range(width + height - 1):
                if d % 2 == 0:  # Even diagonals
                    for x in range(min(d, width - 1), max(0, d - height + 1) - 1, -1):
                        scan_pattern.append((x, d - x))
                else:  # Odd diagonals
                    for y in range(min(d, height - 1), max(0, d - width + 1) - 1, -1):
                        scan_pattern.append((d - y, y))
            return scan_pattern

        # Rearrange the pixels using the Zeta-Z scan pattern
        scan_pattern = zeta_z_scan(width, height)
        rearranged_pixels = [pixels[y * width + x] for x, y in scan_pattern]

        # Create a new image from the rearranged pixels
        encrypted_image = Image.new('RGB', (width, height))
        encrypted_image.putdata(rearranged_pixels)

    # Save the encrypted image
        original_dir, original_filename = os.path.split("cipher")
        cipher_filename = os.path.splitext(original_filename)[0] + "_encrypted.png"
        cipher_path = os.path.join(original_dir, cipher_filename)
        encrypted_image.save(cipher_path)

        # Convert encrypted image to PhotoImage to display in tkinter
        encrypted_photo = ImageTk.PhotoImage(encrypted_image)

        # Update the label with the encrypted image
        label.config(image=encrypted_photo)
        label.image = encrypted_photo
        image_status_label.config(text="Zeta Z Scan \nPattern Image")
        
       

def encrypt_and_display_image():
    file_path = r"cipher_encrypted.png"  # Change the path to your image
    encrypt_image1(file_path)

# Function to encrypt image using Arnold Cat Map
def encrypt_image1(file_path):
    try:
        image = Image.open(file_path)

        image_array = np.array(image)
        encrypted_image = arnold_cat_map(image_array, iterations=50)

        # Get the directory and original file name
        directory = os.path.dirname(file_path)
        file_name = os.path.splitext(os.path.basename(file_path))[0]

        # Generate save path
        save_path = os.path.join(directory, f"{file_name}_arnoldcatmap.png")

        # Save the encrypted image
        encrypted_image_pil = Image.fromarray(encrypted_image)
        encrypted_image_pil.save(save_path)

        # Display the encrypted image
        encrypted_image_tk = ImageTk.PhotoImage(encrypted_image_pil)
        label.config(image=encrypted_image_tk)
        label.image = encrypted_image_tk
        image_status_label.config(text="Confused Image")


    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Function to perform Arnold Cat Map encryption
def arnold_cat_map(image, iterations):
    height, width = image.shape[:2]
    encrypted_image = np.zeros_like(image)

    for i in range(iterations):
        for y in range(height):
            for x in range(width):
                new_x = (2*x + y) % width
                new_y = (x + y) % height
                encrypted_image[new_y, new_x] = image[y, x]

        image = encrypted_image.copy()

    return encrypted_image

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

    return encrypted_image

def logistic_map(x, r):
    return r * x * (1 - x)

def chaotic_map(seed, length):
    x = seed
    chaotic_seq = []
    for _ in range(length):
        x = logistic_map(x,3)  # You can adjust the parameter 'r' as needed
        chaotic_seq.append(x)
    return np.array(chaotic_seq)

def chaotic_map1(seed, length):
    x = seed
    chaotic_seq = []
    for _ in range(length):
        x = logistic_map(x,3.9)  # You can adjust the parameter 'r' as needed
        chaotic_seq.append(x)
    return np.array(chaotic_seq)

def diffusion(image, key_sequence):
    flattened_image = image.flatten()
    diffused_image = flattened_image.copy()

    for i in range(len(flattened_image)):
        diffused_image[i] ^= int(255 * key_sequence[i % len(key_sequence)])

    return diffused_image.reshape(image.shape)

def encrypt_and_diffuse(image_path):
    # Encrypt image using spiral scan pattern 
    encrypted_image = encrypt_image(image_path)

    # Generate key sequence using chaotic map
    key_sequence_length = encrypted_image.shape[0] * encrypted_image.shape[1] * encrypted_image.shape[2]
    seed = 0.5  # Initial seed for chaotic map
    key_sequence = chaotic_map(seed, key_sequence_length)

    # Perform diffusion
    diffused_image = diffusion(encrypted_image, key_sequence)

    return diffused_image

def spiral_in_pattern_reverse(image, spiral_order):
    original_image = np.zeros_like(image)

    for i, (row, col) in enumerate(spiral_order):
        original_image[i // image.shape[1], i % image.shape[1]] = image[row, col]

    return original_image

def reverse_diffusion(image, key_sequence):
    flattened_image = image.flatten()
    diffused_image = flattened_image.copy()

    for i in range(len(flattened_image)):
        diffused_image[i] ^= int(255 * key_sequence[i % len(key_sequence)])

    return diffused_image.reshape(image.shape)

def decrypt_and_reconstruct(image_path):
    # Load the encrypted and diffused image
    encrypted_diffused_image = cv2.imread(image_path)

    # Reverse diffusion using the same chaotic map
    key_sequence_length = encrypted_diffused_image.shape[0] * encrypted_diffused_image.shape[1] * encrypted_diffused_image.shape[2]
    seed = 0.5  # Initial seed for chaotic map
    key_sequence = chaotic_map1(seed, key_sequence_length)
    diffused_image = reverse_diffusion(encrypted_diffused_image, key_sequence)

    # Reverse spiral scan pattern
    spiral_order = spiral_in_pattern(encrypted_diffused_image.shape[0], encrypted_diffused_image.shape[1])
    original_image = spiral_in_pattern_reverse(diffused_image, spiral_order)

    return original_image

def browse_image_encrypt_and_diffuse():
    filename = r"cipher_encrypted_arnoldcatmap.png"  # Change the path to your image

    if filename:
        encrypted_diffused_image = encrypt_and_diffuse(filename)

        img = Image.fromarray(cv2.cvtColor(encrypted_diffused_image, cv2.COLOR_BGR2RGB))
        directory = os.path.dirname(filename)
        file_name = os.path.splitext(os.path.basename(filename))[0]

        # Generate save path
        save_path = os.path.join(directory, f"{file_name}_step3.png")
        if save_path:
            img.save(save_path)
        
        img_tk = ImageTk.PhotoImage(image=img)
        label.config(image=img_tk)
        label.image = img_tk  
        image_status_label.config(text="Diffused Image")


def browse_image_decrypt_and_reconstruct():
    file_name = r"cipher_encrypted_arnoldcatmap_step3.png"  # Change the path to your image

    if file_name:
        original_image = decrypt_and_reconstruct(file_name)
        # Convert the image to PIL format
        img = Image.fromarray(cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB))
        # Convert PIL image to Tkinter PhotoImage
        
        
        # Ask user for filename to save the processed image
        directory = os.path.dirname(file_name)
        file_name = os.path.splitext(os.path.basename(file_name))[0]

        # Generate save path
        save_path = os.path.join(directory, f"{file_name}_step-------3.png")
        if save_path:
            img.save(save_path)
        
        img_tk = ImageTk.PhotoImage(image=img)
        label.config(image=img_tk)
        label.image = img_tk  # Keep a reference to avoid garbage collection
        image_status_label.config(text="Confused Image")








# Function to browse and display the cipher image
def browse_cipher_image():
    global cipher_image
    file_path = filedialog.askopenfilename(title="Select Cipher Image", filetypes=[("Image Files", "*.png *.jpg *.jpeg")])
    if file_path:
        cipher_image = Image.open(file_path)
        cipher_image.thumbnail((500, 300))  # Resize image to fit the canvas
        cipher_image = cipher_image.resize((256,256))  # Custom size: (width, height)
        photo = ImageTk.PhotoImage(cipher_image)  # Convert image to PhotoImage
        label.config(image=photo)  # Update the label with the new image
        label.image = photo  # Keep a reference to the image to prevent it from being garbage collected
        image_status_label.config(text="Cipher Image")








# Function to perform decryption using Arnold Cat Map
def decrypt_arnold_cat_map_image():
    file_path = r"cipher_encrypted_arnoldcatmap_step3_step-------3.png"  # Change the path to your image
    decrypt_image1(file_path)




# Function to decrypt image using Arnold Cat Map
def decrypt_image1(file_path):
    try:
        encrypted_image = Image.open(file_path)

        encrypted_image_array = np.array(encrypted_image)
        decrypted_image = arnold_cat_map_decrypt(encrypted_image_array, iterations=50)

         # Get the directory and original file name
        directory = os.path.dirname(file_path)
        file_name = os.path.splitext(os.path.basename(file_path))[0]

        save_path = os.path.join(directory, f"{file_name}_decryption_arnoldcatmap.png")

        decrypted_image_pil = Image.fromarray(decrypted_image)
        decrypted_image_pil.save(save_path)
        
        # Display the decrypted image
        decrypted_image_pil = Image.fromarray(decrypted_image)
        decrypted_photo = ImageTk.PhotoImage(decrypted_image_pil)
        label.config(image=decrypted_photo)
        label.image = decrypted_photo
        image_status_label.config(text="Zeta Z Scan Pattern\n Image")


    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")


# Function to perform Arnold Cat Map decryption
def arnold_cat_map_decrypt(encrypted_image, iterations):
    height, width = encrypted_image.shape[:2]
    decrypted_image = np.zeros_like(encrypted_image)

    for i in range(iterations):
        for y in range(height):
            for x in range(width):
                new_x = (x - y) % width
                new_y = (-x + 2*y) % height
                decrypted_image[new_y, new_x] = encrypted_image[y, x]

        encrypted_image = decrypted_image.copy()

    return decrypted_image


def decrypted_scan_pattern_output():
    file_path = r"cipher_encrypted_arnoldcatmap_step3_step-------3_decryption_arnoldcatmap.png" # Change the path to your image
    decrypt_image(file_path)

# Function to perform decryption and display the decrypted image
def decrypt_image(file_path):
    decrypted_image2 = Image.open(file_path)

    if decrypted_image2:
        # Get image size
        width, height = decrypted_image2.size

        # Get pixels of the cipher image
        pixels = list(decrypted_image2.getdata())

        # Define the Zeta-Z scan pattern
        def zeta_z_scan(width, height):
            scan_pattern = []
            for d in range(width + height - 1):
                if d % 2 == 0:  # Even diagonals
                    for x in range(min(d, width - 1), max(0, d - height + 1) - 1, -1):
                        scan_pattern.append((x, d - x))
                else:  # Odd diagonals
                    for y in range(min(d, height - 1), max(0, d - width + 1) - 1, -1):
                        scan_pattern.append((d - y, y))
            return scan_pattern

        # Get the Zeta-Z scan pattern
        scan_pattern = zeta_z_scan(width, height)

        # Rearrange the pixels back to original order
        original_pixels = [(0, 0)] * (width * height)
        for i, (x, y) in enumerate(scan_pattern):
            original_pixels[y * width + x] = pixels[i]

        # Create a new image from the decrypted pixels
        decrypted_image2 = Image.new('RGB', (width, height))
        decrypted_image2.putdata(original_pixels)

        # Convert decrypted image to PhotoImage to display in tkinter
        decrypted_photo1 = ImageTk.PhotoImage(decrypted_image2)

        # Update the label with the decrypted image
        label.config(image=decrypted_photo1)
        label.image = decrypted_photo1
        image_status_label.config(text="Original Image")



active_button = None

# Function to set the active button and change its background color
def set_active_button(button):
    global active_button
    if active_button:
        active_button.config(bg="SystemButtonFace")  # Reset previous active button color
    active_button = button
    active_button.config(bg="sky blue")  # Set new active button color
# Function to reset the displayed image and clear global variables
# Function to reset the displayed image and clear global variables
def reset_image():
    global original_image, encrypted_image, cipher_image, decrypted_image
    original_image = None
    encrypted_image = None
    cipher_image = None
    decrypted_image = None

    # Clear the image label
    label.config(image=None)
    label.image = None  # Reset the reference to the image to prevent it from being garbage collected
    image_status_label.config(text="")

# Create a reset button
reset_button = tk.Button(root, text="Reset", command=reset_image, width=10, height=2, font=("Helvetica", 10, "bold"))
reset_button.place(x=button_x+670, y=button_y+330)

title_label = tk.Label(root, text="IMAGE SECURITY USING SCAN PATTERN AND CHAOTIC MAP", font=("Helvetica", 18, "bold"),fg="magenta")
title_label.pack()

encryption_label=tk.Label(root,text="ENCRYPTION",font=("Helvetica", 16, "bold"),fg="blue")
encryption_label.place(x=575,y=100)
# Create buttons for image operations
browse_button = tk.Button(root, text="Browse Image", command=lambda: (set_active_button(browse_button), browse_image()), width=20, height=2,font=("Helvetica", 8,"bold"))
browse_button.place(x=button_x+555, y=button_y+50)

zeta_z_button = tk.Button(root, text="Scan Pattern \nEncryption Image", command=lambda: (set_active_button(zeta_z_button),zeta_z_operation()), width=20, height=3,font=("Helvetica", 8, "bold"))
zeta_z_button.place(x=button_x+555, y=button_y+100)

confusion_button = tk.Button(root, text="Arnold Cat Map Encryption\n( confusion )", command=lambda:(set_active_button(confusion_button), encrypt_and_display_image()), width=20, height=3,font=("Helvetica", 8, "bold"))
confusion_button.place(x=button_x+555, y=button_y+165)

diffusion_button=tk.Button(root, text="Diffusion operation",command=lambda:(set_active_button(diffusion_button), browse_image_encrypt_and_diffuse()), width=20, height=2,font=("Helvetica", 8, "bold"))
diffusion_button.place(x=button_x+555,y=button_y+230)



#decryption part##################################

decryption_label=tk.Label(root,text="DECRYPTION",font=("Helvetica", 16, "bold"),fg="blue")
decryption_label.place(x=575,y=450)

browse_cipher_button = tk.Button(root, text="Browse Cipher Image", command=lambda:(set_active_button(browse_cipher_button),browse_cipher_image()), width=20, height=2,font=("Helvetica", 8, "bold"))
browse_cipher_button.place(x=button_x+555, y=button_y+400)

reverse_diffusion_button=tk.Button(root, text="Reverse Diffusion \n operation",command=lambda:(set_active_button(reverse_diffusion_button), browse_image_decrypt_and_reconstruct()), width=20, height=3,font=("Helvetica", 8, "bold"))
reverse_diffusion_button.place(x=button_x+555,y=button_y+450)

arnoldcatdecryption = tk.Button(root, text="Arnold Cat Map \nDecryption\n(Reverse confusion)", command=lambda:(set_active_button(arnoldcatdecryption),decrypt_arnold_cat_map_image()), width=20, height=3,font=("Helvetica", 8, "bold"))
arnoldcatdecryption.place(x=button_x+555, y=button_y+515)

decrypt_button = tk.Button(root, text="Reverse of Scan \n  Pattern", command=lambda:(set_active_button(decrypt_button),decrypted_scan_pattern_output()), width=20, height=3,font=("Helvetica", 8, "bold"))
decrypt_button.place(x=button_x+555, y=button_y+580)


root.mainloop()
