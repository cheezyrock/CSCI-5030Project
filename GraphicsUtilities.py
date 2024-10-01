import tkinter as tk
from functools import partial
class GraphicsUtilities:
    def __init__(self, game):
        self.game = game
        self.root = tk.Tk()
        self.root.title("Narrative Game")

        # Create widgets
        self.narrative_label = tk.Label(self.root, text="", wraplength=400)
        self.narrative_label.pack()

        self.choice_buttons_frame = tk.Frame(self.root)
        self.choice_buttons_frame.pack()

        self.update_ui()

    def update_ui(self):
        
        self.narrative_label.config(text=self.game.get_current_narrative())

        
        for widget in self.choice_buttons_frame.winfo_children():
            widget.destroy()

        
        choices = self.game.get_current_choices()
        for i, (choice_text, _) in enumerate(choices):
            button = tk.Button(self.choice_buttons_frame, text=choice_text,
                               command=partial(self.handle_choice, i))
            button.pack()

    def handle_choice(self, choice_index):
        self.game.make_choice(choice_index)
        if self.game.is_game_over():
            self.display_game_over()
        else:
            self.update_ui()

    def display_game_over(self):
        # Clear the screen and show game over message
        self.narrative_label.config(text="Game Over!")
        for widget in self.choice_buttons_frame.winfo_children():
            widget.destroy()

    def run(self):
        self.root.mainloop()
