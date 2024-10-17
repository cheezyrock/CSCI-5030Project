from PIL import Image, ImageTk
class ImageHandler:
    @staticmethod
    def load_image(image_path, size=(300,300)):
        img = Image.open(image_path)
        img = img.resize(size, Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(img)

