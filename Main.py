# https://github.com/TkinterEP/ttkthemes/tree/master/screenshots

import torch, os
from torch.fx.experimental.migrate_gradual_types.constraint_transformation import register_transformation_rule
from torchvision import models, transforms
from PIL import Image

import tkinter as tk, threading
from ttkthemes import ThemedTk
from tkinter import ttk

# ===============================================================================

cooldown = False


def predict_image(model, image_tensor):
    try:
        with torch.no_grad():
            outputs = model(image_tensor)
            _, predicted = torch.max(outputs, 1)
            class_idx = predicted.item()

            if class_idx in range(1, 7) or class_idx in range(390, 398): return "Fish"
            elif class_idx in range(151, 269): return "Dog"
            elif class_idx in range(281, 288): return "Cat"
            elif class_idx in range(53, 69): return "Snake"
            elif class_idx in range(8, 25) or class_idx in range(81, 97) or class_idx in range(128, 147): return "Bird"
            elif class_idx in range(322, 327): return "Butterfly"

            else: return "Unknown"


    except Exception as e:
        title_label.configure(text=f"Error predicting: {str(e)}", background="red")
        root.after(2000, reset_title)

def load_model():
    model = models.resnet18(pretrained = True)
    model.eval()
    return model

def preprocess_image(image_path):
    try:
        transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(
                mean = [0.485, 0.456, 0.406],
                std = [0.229, 0.224, 0.225]
            )
        ])
        image = Image.open(image_path).convert("RGB")
        image_tensor = transform(image)
        image_tensor = image_tensor.unsqueeze(0)
        return image_tensor


    except Exception as e:
        title_label.configure(text=f"Error loading image: {str(e)}", background="red")
        root.after(2000, reset_title)

def main():
    global cooldown
    if cooldown: return
    cooldown = True
    identify_button.configure(state = "disabled")

    image_path = path_entry.get()

    if not os.path.exists(image_path):
        title_label.configure(text = "Invalid path!", background = "red")
        root.after(2000, reset_title)
        return

    image_tensor = preprocess_image(image_path)

    prediction = predict_image(model, image_tensor)
    print(f"Prediction: {prediction}")
    prediction_label.configure(text = f"Prediction: {prediction}")
    identify_button.configure(state = "normal")
    cooldown = False

def reset_title():
    global cooldown
    title_label.configure(text = "Image Identifier!", background = "light blue")
    identify_button.configure(state = "normal")
    cooldown = False

# ==========================================================

root = ThemedTk(theme = "breeze")

screen_width = 600
screen_height = 340

screen_width_middle = int(root.winfo_screenwidth() / 2 - screen_width / 2)
screen_height_middle = int(root.winfo_screenheight() / 2 - screen_height / 2)

root.geometry(f"{screen_width}x{screen_height}+{screen_width_middle}+{screen_height_middle}")
root.title("Arch Creator! - Python Project")
root.configure(themebg="breeze")
root.resizable(False, False)

root.lift()
root.focus_force()

# ---------------------------------------------------------------

button_style = ttk.Style()
button_style.configure("TButton", font = ("Rubik Mono One", 20))


title_label = tk.Label(root, text = "Image Identifier!", background = "light blue", font = ("Rubik Mono One", 25))
title_label.pack(pady = 30)

# ---------------------------------------------------------------

path_frame = tk.Frame(root)
path_frame.pack(pady = 5)


path_label = tk.Label(path_frame, text = "Path:", font = ("Rubik Mono One", 15))
path_label.pack(side = tk.LEFT)

path_entry = ttk.Entry(path_frame, font = ("Arial", 15), width = 33)
path_entry.pack(padx = 30, side = tk.LEFT)

# ---------------------------------------------------------------

identify_button = ttk.Button(root, text = "Indentify!", style = "TButton", command = main)
identify_button.pack(pady = 20)

# ---------------------------------------------------------------

prediction_label = tk.Label(root, text = "Prediction: None", font = ("Rubik Mono One", 25), background = "light blue")
prediction_label.pack(pady = 15)

# ================================================================

model = load_model()
root.mainloop()