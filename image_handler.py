import os
from pickle import NONE


from PIL import Image, ImageTk
class ImageHandler:
    @staticmethod
    def load_image(image_name, size=(300,300)):
        filepath = os.path.join(os.getcwd(), 'GameAssets', 'Images', image_name)
        if (os.path.exists(filepath) and image_name != ''):
            img = Image.open(filepath)
            img = img.resize(size, Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(img)

        return NONE
