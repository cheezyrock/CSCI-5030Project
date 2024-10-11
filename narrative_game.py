import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

class StoryNode:
    def __init__(self, text, choices, image_path=None):
        self.text = text
        self.choices = choices
        self.image_path = image_path

class Game:
    def __init__(self):
        self.story = self.create_story()
        self.current_node = self.story

        # Set up the main window
        self.root = tk.Tk()
        self.root.title("Interactive Story Game")
        
        self.story_text = tk.StringVar()
        self.story_label = tk.Label(self.root, textvariable=self.story_text, wraplength=300)
        self.story_label.pack(pady=20)

        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=20)

        self.image_label = tk.Label(self.root)
        self.image_label.pack()
        
        
        self.play()

        self.root.mainloop()

    def create_story(self):
        # End node
        end_node = StoryNode("Your adventure ends here. Thanks for playing!", [])

        # Story nodes
        choice_6 = StoryNode("You are at the edge of the forest. What do you do?", [
            StoryNode("Go back", [end_node], "images/explore.jpeg"),
            StoryNode("Jump from the edge", [end_node], "images/camp site.jpeg"),
        ])

        choice_5 = StoryNode("A wise man offers potions. Which do you choose?", [
            StoryNode("Strength potion.", [choice_6]),
            StoryNode("Wisdom potion.", [choice_6]),
            StoryNode("Invisibility potion.", [choice_6])
        ])

        choice_4 = StoryNode("A fork in the road. Go left or right?", [
            StoryNode("Left to the mountains.", [choice_5]),
            StoryNode("Right to the valley.", [choice_5]),
            StoryNode("Go back.", [end_node])
        ])

        choice_3 = StoryNode("A dragon appears! What do you do?", [
            StoryNode("Fight!", [choice_4]),
            StoryNode("Flee.", [choice_4]),
            StoryNode("Negotiate.", [choice_4])
        ])

        choice_2 = StoryNode("You find a map. What now?", [
            StoryNode("Follow it.", [choice_3],"./Images/map-follow.png"),
            StoryNode("Ignore it.", [choice_3],"./Images/map-ignore.png"),
            StoryNode("Burn it.", [end_node],"./Images/map-burn.png" )
        ])

        choice_1 = StoryNode("You awaken in a strange land. What next?", [
            StoryNode("Explore.", [choice_2],"./Images/exploring.png"),
            StoryNode("Seek help.", [choice_2],"./Images/seek-help.png"),
            StoryNode("Camp.", [end_node],"./Images/camping.png")
        ],"./Images/lush-garden.jpeg")

        # Starting point
        start_node = StoryNode("You find yourself in a lush, unfamiliar land.", [
            choice_1,
        ], "./Images/start-image.png")

        return start_node

    def display_choices(self):
        # Clear existing buttons
        for widget in self.button_frame.winfo_children():
            widget.destroy()

        self.story_text.set(self.current_node.text)
        
        if self.current_node.image_path:
            self.display_image(self.current_node.image_path)

        if self.current_node.choices:
            for i, choice in enumerate(self.current_node.choices):
                button = tk.Button(self.button_frame, text=choice.text, command=lambda index=i: self.make_choice(index))
                button.pack(pady=5)
        else:
            messagebox.showinfo("Game Over", self.current_node.text)
            self.root.quit()
            
    def display_image(self, image_path):
            img = Image.open(image_path)
            img = img.resize((300, 300), Image.Resampling.LANCZOS)
            img = ImageTk.PhotoImage(img)
            self.image_label.config(image=img)
            self.image_label.image = img

    def make_choice(self, index):
        self.current_node = self.current_node.choices[index]
        self.display_choices()

    def play(self):
        self.display_choices()

# Start the game
if __name__ == "__main__":
    Game()
