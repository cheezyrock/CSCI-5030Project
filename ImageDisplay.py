import tkinter as tk
from PIL import Image, ImageTk

def display_jpeg_image(image_path, width,height):
    root = tk.Tk()
    root.title("JPEG Image Display")

    img = Image.open(image_path)
    img = img.resize((width, height), Image.Resampling.LANCZOS)

    img = ImageTk.PhotoImage(img)

    label = tk.Label(root, image=img)
    label.pack()


    root.mainloop()

# Example usage
display_jpeg_image("./Images/map.png", 300,300)
