import unittest
from PIL import ImageTk
from image_handler import ImageHandler
from story_node import StoryNode
import tkinter as tk

class TestImageHandler(unittest.TestCase):

    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()

    def tearDown(self):
        self.root.destroy()

    def test_load_image(self):
        story_node = StoryNode("Test text", [], "./Images/lush-garden.jpeg")
        image_path = story_node.image_path
        try:
            img = ImageHandler.load_image(image_path)
            self.assertIsInstance(img, ImageTk.PhotoImage, "Loaded image should be an instance of ImageTk.PhotoImage")
        except FileNotFoundError:
            self.fail(f"Image file '{image_path}' not found.")
        
        except Exception as e:
            self.fail(f"An error occurred: {e}")

if __name__ == "__main__":
    unittest.main()