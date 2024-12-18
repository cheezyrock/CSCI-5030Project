import tkinter as tk
import os
from tkinter import messagebox
from story_builder import StoryBuilder
from image_handler import ImageHandler
import Audio
import asyncio
import threading
import socket
from DecisionPoints import Player, DecisionPointsUI, GameIntegration
import itertools
from PIL import Image, ImageTk
from tkinter import font as tkfont

class Game:
    def __init__(self):
        self.peers = []
        self.story = StoryBuilder.create_story()
        self.current_node = self.story
        self.players = [Player(player_id=i) for i in range(1, 3)]  # Example: two players
        self.decision_manager = GameIntegration(self.players, DecisionPointsUI(self.players))
        self.story_font = ('Luckiest Guy', 20, 'bold')
        self.choice_font = ('Luckiest Guy', 15, 'bold')
        
        # Set up the main window
        self.root = tk.Tk()
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=20)
        self.root.title("Interactive Story Game")
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.minsize(400, 400)
        
        # Load background image
        bg_image_path = os.path.join("GameAssets", "images", "background.png")
        if os.path.exists(bg_image_path):
            bg_image = Image.open(bg_image_path)
            bg_image = bg_image.resize((1300, 1300))  # Resize to fit window
            self.bg_photo = ImageTk.PhotoImage(bg_image)
        else:
            self.bg_photo = None
            print(f"Background image not found at: {bg_image_path}")

        # Set background
        
        if self.bg_photo:
            self.bg_label = tk.Label(self.root, image=self.bg_photo)
        else:
            self.bg_label = tk.Label(self.root, bg="black")
        self.bg_label.place(relwidth=1, relheight=1)  # Stretch to fill the window

        # Create a frame for widgets to overlay on the background
        self.widget_frame = tk.Frame(self.root, bg="#000000")
        self.widget_frame.pack(expand=True)

        self.story_text = tk.StringVar()
        self.rainbow_colors = itertools.cycle(["#ff0000", "#ff7f00", "#ffff00",
                                               "#00ff00", "#0000ff", "#4b0082", "#9400d3"])

        # Welcome message
        self.welcome_label = tk.Label(
            self.root,
            text="🎉 Welcome to the Interactive Story Game!!! 🎉",
            font=('Luckiest Guy', 20, 'bold'),
            fg="#ffffff",
            bg="#000000",
            pady=15,
            padx=20,
            borderwidth=8,
            relief="ridge",
            highlightbackground="#ffffff",
            highlightthickness=3,
            anchor="center"
        )
        self.welcome_label.pack(pady=20)
        self.update_rainbow()

        # Story display label
        self.story_label = tk.Label(self.root, textvariable=self.story_text, wraplength=300, font=self.story_font,pady=10)
        self.story_label.pack(pady=10)

        # Button frame
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=20)

        self.image_label = tk.Label(self.root)
        self.image_label.pack()

       # Add buttons for hosting or joining a game
        self.host_button = self.style_button("Host Game", self.host_game)
        self.join_button = self.style_button("Join Game", self.show_ip_entry)
        
        self.host_button.pack(side=tk.TOP, pady=20)  
        self.join_button.pack(side=tk.TOP, pady=20)  

        # Create an IP address entry field (hidden by default)
        self.ip_label = tk.Label(self.root, text="Enter Host IP Address:",font=self.story_font)
        self.ip_entry = tk.Entry(self.root, width=20,font=self.story_font)
        self.ip_submit_button = tk.Button(self.root, text="Join", command=self.join_game)

        self.ip_label.pack_forget()
        self.ip_entry.pack_forget()
        self.ip_submit_button.pack_forget()

        Audio.BGM.playBGM()

        self.connected_players = []

        self.root.mainloop()

    
    
    def style_button(self, text, command, width=20, height=1, font=('Luckiest Guy', 16, 'bold'), bg="#000000", fg="#2196f3"):
        """Helper function to style buttons consistently."""
        return tk.Button(
            self.root,
            text=text,
            command=command,
            width=width,
            height=height,
            font=font,
            bg=bg,
            fg=fg,
            relief="raised",
            borderwidth=3
        )

    def update_rainbow(self):
        """Update the welcome label's text color to create a rainbow effect."""
        self.welcome_label.config(fg=next(self.rainbow_colors))
        self.root.after(500, self.update_rainbow)

    def display_choices(self):
        """Display the story choices for the player."""
        for widget in self.button_frame.winfo_children():
            widget.destroy()  # Clear existing buttons

        self.story_text.set(self.current_node.text)

        if self.current_node.image_path:
            img = ImageHandler.load_image(self.current_node.image_path)
            self.image_label.config(image=img)
            self.image_label.image = img

        if self.current_node.choices:
            for i, choice in enumerate(self.current_node.choices):
                button = tk.Button(self.button_frame, text=choice.text, command=lambda index=i: self.make_choice(index),font=self.choice_font, bg="#000000",  
            fg="#2196f3")
                button.pack(side=tk.LEFT, padx=5, pady=5)
        else:
            messagebox.showinfo("Game Over", self.current_node.text)
            self.root.quit()

    def make_choice(self, index):
        """Update the game state based on the player's choice."""
        self.current_node = self.current_node.choices[index]
        Audio.SFX.playSFX("ButtonPress.wav")
        self.display_choices()

    def finalize_group_decision(self, group_decision):
        """Process the group decision and update player decision points."""
        self.decision_manager.handle_group_decision(group_decision)
        self.decision_manager.decision_manager.display_dp()

    def play(self):
        """Start the game."""
        self.display_choices()
        
    def change_background_to_black(self):
        """Change the root window's background to black and update widgets."""
        self.root.config(bg="black")  
        self.bg_label.config(bg="black", image="") 
        self.widget_frame.config(bg="black")  
        self.story_label.config(bg="black", fg="white") 
        self.image_label.config(bg="black")  
        self.ip_label.config(bg="black", fg="white")    
        self.ip_entry.config(bg="black", fg="white", insertbackground="white") 
        self.ip_submit_button.config(bg="black", fg="white")
    
    def host_game(self):
        """Host a new game and start listening for incoming connections."""
        self.change_background_to_black()
        threading.Thread(target=asyncio.run, args=(self.start_host_server(),)).start()
        print("Hosting game...")
        self.remove_main_buttons()  # Remove Host and Join buttons

    def start_game(self):
        """Start the game logic for the host after hosting the game."""
        self.play()  # Start the game loop for the host

    async def start_host_server(self):
        """Start a server that allows players to connect."""
        server = await asyncio.start_server(self.handle_client, 'localhost', 8888)
        async with server:
            print(f"Hosting game on localhost:8888")
            await server.serve_forever()

    async def handle_client(self, reader, writer):
        """Handle incoming client connections and share game data."""
        print("A player has connected.")
        self.connected_players.append(writer)  # Add the connected player to the list

        # Send the initial game state to the connected player
        writer.write(self.current_node.text.encode())
        await writer.drain()

        # Call check to see if both players are connected
        self.start_game()

    def show_ip_entry(self):
        """Show the IP entry fields when joining a game."""
        self.ip_label.pack(pady=10)
        self.ip_entry.pack(pady=10)
        self.ip_submit_button.pack(pady=10)
        self.remove_main_buttons()  # Remove Host and Join buttons

    def join_game(self):
        """Allow the user to input a host's IP and connect to an existing game."""
        peer_ip = self.ip_entry.get()
        if peer_ip:
            threading.Thread(target=asyncio.run, args=(self.connect_to_host(peer_ip, 8888),)).start()
            print(f"Attempting to join game at {peer_ip}...")
            self.ip_label.pack_forget()  # Hide input after submitting
            self.ip_entry.pack_forget()
            self.ip_submit_button.pack_forget()
            self.remove_main_buttons()  # Remove Host and Join buttons
            self.change_background_to_black()
        else:
            messagebox.showerror("Error", "Please enter a valid IP address.")

    async def connect_to_host(self, host, port):
        """Connect to an existing game hosted by another player."""
        try:
            reader, writer = await asyncio.open_connection(host, port)
            game_intro = await reader.read(100)  # Receive initial story data
            self.story_text.set(game_intro.decode())
            self.display_choices()  # Show the story after joining
        except Exception as e:
            messagebox.showerror("Connection Error", f"Failed to connect to the game: {e}")

    def remove_main_buttons(self):
        """Hide the Host and Join buttons after game starts."""
        self.host_button.pack_forget()
        self.join_button.pack_forget()

    def on_close(self):
        """Terminate the game server when closing the window."""
        print("Closing the game...")
        self.root.quit()  # Close the window
        # Here you can add logic to stop the server or close any active connections if necessary
        # For example, if you are running a server, you should properly stop it before quitting

if __name__ == "__main__":
    game = Game()