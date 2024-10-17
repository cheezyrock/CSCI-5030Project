#class Game:
#    def __init__(self,player, story_nodes):
#        self.player = player
#        self.story_nodes = story_nodes
#        self.current_node = story_nodes[0] 
#
#    def get_current_narrative(self):
#        return self.current_node.get_narrative()
#
#    def get_current_choices(self):
#        return self.current_node.get_choices()
#
#    def make_choice(self, choice_index):
#        """Make a choice, update the current story node"""
#        next_node = self.current_node.get_choices()[choice_index][1]
#        self.current_node = next_node
#
#    def is_game_over(self):
#        return len(self.current_node.get_choices()) == 0  
#
# game.py

import tkinter as tk
from tkinter import messagebox
from story_builder import StoryBuilder
from image_handler import ImageHandler
import Audio

class Game:
    def __init__(self):
        self.story = StoryBuilder.create_story()
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

        Audio.BGM.playBGM()
        self.play()
        self.root.mainloop()

    def display_choices(self):
        # Clear existing buttons
        for widget in self.button_frame.winfo_children():
            widget.destroy()

        self.story_text.set(self.current_node.text)

        if self.current_node.image_path:
            img = ImageHandler.load_image(self.current_node.image_path)
            self.image_label.config(image=img)
            self.image_label.image = img

        if self.current_node.choices:
            for i, choice in enumerate(self.current_node.choices):
                button = tk.Button(self.button_frame, text=choice.text, command=lambda index=i: self.make_choice(index))
                button.pack(pady=5)
        else:
            messagebox.showinfo("Game Over", self.current_node.text)
            self.root.quit()

    def make_choice(self, index):
        self.current_node = self.current_node.choices[index]
        Audio.SFX.playSFX("ButtonPress.wav")
        self.display_choices()

    def play(self):
        self.display_choices()
