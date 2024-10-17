import customtkinter as ctk
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
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.root = ctk.CTk()
        self.root.title("Interactive Story Game")

        self.story_text = ctk.StringVar()
        self.story_label = ctk.CTkLabel(self.root, textvariable=self.story_text, wraplength=300, font=('Arial', 16))
        self.story_label.pack(pady=20)

        self.image_label = ctk.CTkLabel(self.root)
        self.image_label.pack(pady=20)

        self.button_frame = ctk.CTkFrame(self.root)
        self.button_frame.pack(pady=20)

        self.play()

        self.root.mainloop()

    def create_story(self):
        end_node = StoryNode("Your adventure ends here. Thanks for playing!", [], "path/to/end_image.png")

        choice_6 = StoryNode("You are at the edge of the forest. What do you do?", [
            StoryNode("Go back", [end_node], "path/to/back_image.png"),
            StoryNode("Jump from the edge", [end_node], "path/to/jump_image.png"),
        ], "path/to/forest_edge_image.png")

        choice_5 = StoryNode("A wise man offers potions. Which do you choose?", [
            StoryNode("Strength potion.", [choice_6], "path/to/strength_potion_image.png"),
            StoryNode("Wisdom potion.", [choice_6], "path/to/wisdom_potion_image.png"),
            StoryNode("Invisibility potion.", [choice_6], "path/to/invisibility_potion_image.png")
        ], "path/to/wise_man_image.png")

        choice_4 = StoryNode("A fork in the road. Go left or right?", [
            StoryNode("Left to the mountains.", [choice_5], "path/to/mountains_image.png"),
            StoryNode("Right to the valley.", [choice_5], "path/to/valley_image.png"),
            StoryNode("Go back.", [end_node], "path/to/back_image.png")
        ], "path/to/fork_image.png")

        choice_3 = StoryNode("A dragon appears! What do you do?", [
            StoryNode("Fight!", [choice_4], "path/to/fight_image.png"),
            StoryNode("Flee.", [choice_4], "path/to/flee_image.png"),
            StoryNode("Negotiate.", [choice_4], "path/to/negotiate_image.png")
        ], "path/to/dragon_image.png")

        choice_2 = StoryNode("You find a map. What now?", [
            StoryNode("Follow it.", [choice_3], "path/to/follow_map_image.png"),
            StoryNode("Ignore it.", [choice_3], "path/to/ignore_map_image.png"),
            StoryNode("Burn it.", [end_node], "path/to/burn_map_image.png")
        ], "path/to/map_image.png")

        choice_1 = StoryNode("You awaken in a strange land. What next?", [
            StoryNode("Explore.", [choice_2], "path/to/explore_image.png"),
            StoryNode("Seek help.", [choice_2], "path/to/seek_help_image.png"),
            StoryNode("Camp.", [end_node], "path/to/camp_image.png")
        ], "path/to/awakening_image.png")

        start_node = StoryNode("You find yourself in a lush, unfamiliar land.", [
            choice_1,
        ], "path/to/start_image.png")

        return start_node

    def display_choices(self):
        for widget in self.button_frame.winfo_children():
            widget.destroy()

        self.story_text.set(self.current_node.text)

        # Display the image if available
        if self.current_node.image_path:
            image = Image.open(self.current_node.image_path)
            image = image.resize((300, 200), Image.ANTIALIAS)  # Resize image to fit
            self.image = ImageTk.PhotoImage(image)
            self.image_label.configure(image=self.image)
            self.image_label.image = self.image  # Keep a reference to avoid garbage collection

        if self.current_node.choices:
            for i, choice in enumerate(self.current_node.choices):
                button = ctk.CTkButton(self.button_frame, text=choice.text, command=lambda index=i: self.make_choice(index))
                button.pack(pady=5)
        else:
            messagebox.showinfo("Game Over", self.current_node.text)
            self.root.quit()

    def make_choice(self, index):
        self.current_node = self.current_node.choices[index]
        self.display_choices()

    def play(self):
        self.display_choices()

# Start the game
if __name__ == "__main__":
    Game()
