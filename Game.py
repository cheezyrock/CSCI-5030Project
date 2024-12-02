import tkinter as tk
import os
from tkinter import messagebox
from story_builder import StoryBuilder
from image_handler import ImageHandler
import Audio
import asyncio
import threading
import socket
from DecisionPoints import Player,DecisionPointsUI,GameIntegration
import itertools
from PIL import Image, ImageTk

class Game:
    def _init_(self):
        self.peers = []
        self.story = StoryBuilder.create_story()
        self.current_node = self.story
        self.players = [Player(player_id=i) for i in range(1,3)]  # Example: two players
        self.decision_manager = GameIntegration(self.players, DecisionPointsUI(self.players))
        # Set up the main window
        self.root = tk.Tk()
        self.root.title("Interactive Story Game")
        
        
        # Register the close event to ensure proper termination
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        bg_image_path = os.path.join("GameAssets", "images", "background.png")
         # Load background image
        bg_image = Image.open(bg_image_path)  # Replace with your image file
        bg_image = bg_image.resize((1300, 1300))  # Resize to fit window
        self.bg_photo = ImageTk.PhotoImage(bg_image)
        
        # Set background
        self.bg_label = tk.Label(self.root, image=self.bg_photo)
        self.bg_label.place(relwidth=1, relheight=1)  # Stretch to fill the window

        # Create a frame for widgets to overlay on the background
        self.widget_frame = tk.Frame(self.root, bg="#000000")  # Transparent frame
        self.widget_frame.pack(expand=True)

        self.story_text = tk.StringVar()
        self.rainbow_colors = itertools.cycle(["#ff0000", "#ff7f00", "#ffff00", 
                                               "#00ff00", "#0000ff", "#4b0082", "#9400d3"])
        # Welcome message
        
       # self.welcome_label = tk.Label(self.root, text="Welcome to the Interactive Story Game!", font=('Comic Sans MS', 18, 'bold'), pady=20)
       #    # Welcome message
        self.welcome_label = tk.Label(
            self.root,
            text="🎉 Welcome to the Interactive Story Game!!! 🎉",
            font=('Sans Comic MS', 20, 'bold'),
            fg="#ffffff",  
            bg="#000000",  
            pady=15,
            padx=20,
            borderwidth=8,
            relief="ridge",
            highlightbackground="#ffffff",  # Optional white outline for emphasis
            highlightthickness=3,  # Thickness of the outline
            anchor="center"# 3D effect
        )
        self.welcome_label.pack(pady=20)
        self.update_rainbow()

        # Story display label
        self.story_label = tk.Label(self.root, textvariable=self.story_text, wraplength=300)
        self.story_label.pack(pady=20)

        # Button frame
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=20)

        self.image_label = tk.Label(self.root)
        self.image_label.pack()

        # Add buttons for hosting or joining a game
        self.host_button = tk.Button(self.root, text="Host Game", command=self.host_game, width=20)
        self.join_button = tk.Button(self.root, text="Join Game", command=self.show_ip_entry, width=20)
        
        self.host_button.pack(side=tk.TOP, pady=10)
        self.join_button.pack(side=tk.TOP, pady=10)

        # Create an IP address entry field (hidden by default)
        self.ip_label = tk.Label(self.root, text="Enter Host IP Address:")
        self.ip_entry = tk.Entry(self.root, width=20)
        self.ip_submit_button = tk.Button(self.root, text="Join", command=self.join_game)

        self.ip_label.pack_forget()  # Hide initially
        self.ip_entry.pack_forget()  # Hide initially
        self.ip_submit_button.pack_forget()  # Hide initially

        Audio.BGM.playBGM()

        self.root.mainloop()

    
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
                button = tk.Button(self.button_frame, text=choice.text, command=lambda index=i: self.make_choice(index))
                button.pack(pady=5)
        else:
            messagebox.showinfo("Game Over", self.current_node.text)
            self.root.quit()

    def make_choice(self):
        
        """Update the game state based on the player's choice."""
        
        self.current_node = self.current_node.choices[index]
        Audio.SFX.playSFX("ButtonPress.wav")
        self.display_choices()
    def finalize_group_decision(self, group_decision):
        """Process the group decision and update player decision points."""
        self.decision_manager.handle_group_decision(group_decision)
        # Display updated decision points for each player
        self.decision_manager.decision_manager.display_dp()

    def play(self):
        """Start the game."""
        self.display_choices()

    # P2P Networking Methods
    def host_game(self):
        """Host a new game and start listening for incoming connections."""
        threading.Thread(target=asyncio.run, args=(self.start_host_server(),)).start()
        print("Hosting game...")
        self.remove_main_buttons()  # Remove Host and Join buttons
        self.start_game()
        asyncio.run(self.start_host_server())
         
    def start_game(self):
        for player in self.peers:
            if player not in self.peers:
                print("Player not found in peers.")
            return
        """Start the game logic for the host after hosting the game."""
        self.play()  # Start the game loop for the host

    async def start_host_server(self):
        """Start a server that allows players to connect."""
        server = await asyncio.start_server(self.handle_client, 'localhost', 8888)
        async with server:
            print(f"Hosting game on localhost:8888")
            await server.serve_forever()
    
    async def handle_client(self, reader, writer):
    # Get the player's information (e.g., IP address or name)
        player = writer.get_extra_info('peername')
    
    # Check if the player is already in the peers list
        if player in self.peers:
            print(f"Player {player} is already connected.")
            return  # You could close the connection here if necessary
    
    # If the player is not already in peers, add them
        self.peers.append(player)
        print(f"Player connected: {player}")
    
    # Continue handling the connection (sending messages, updating game state, etc.)
        try:
        # Handle communication with the player
            while True:
                data = await reader.read(100)
                if not data:
                    break
            writer.write(data)
            await writer.drain()
        except asyncio.CancelledError:
            pass
        finally:
        # Remove player when done
            self.peers.remove(player)
            print(f"Player disconnected: {player}")
            writer.close()
            await writer.wait_closed()

   # async def handle_client(self, reader, writer):
   #     player = writer.get_extra_info('peername')
   #     print(f"Player connected: {player}")
    
    # Add the player to the peers list
        self.peers.append(player)
        """Handle incoming client connections and share game data."""
        print("A player has connected.")
        # Send the initial game state to the connected player
        writer.write(self.current_node.text.encode())
        await writer.drain()

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
           # threading.Thread(target=asyncio.run, args=(self.connect_to_host(peer_ip, 8888),)).start()
            print(f"Attempting to join game at {peer_ip}...")
            self.ip_label.pack_forget()  # Hide input after submitting
            self.ip_entry.pack_forget()
            self.ip_submit_button.pack_forget()
            self.remove_main_buttons()  
            
            # Remove Host and Join buttons
            asyncio.run(self.connect_to_host(peer_ip, 8888))
        else:
            messagebox.showerror("Error", "Please enter a valid IP address.")

    async def connect_to_host(self, host, port):
        """Connect to an existing game hosted by another player."""
        try:
            reader, writer = await asyncio.open_connection(host, port)
            self.peers.append((reader,writer))
            print(f"Connected to game at {host}:{port}")
            
            game_intro = await reader.read(100)  # Receive initial story data
            self.story_text.set(game_intro.decode())
            self.display_choices()  # Show the story after joining
        except Exception as e:
            messagebox.showerror("Connection Error", f"Failed to connect to the game: {e}")
    def show_decision_points(self):
        """Display the decision points for each player."""
        self.decision_manager.decision_manager.display_dp()

    def remove_main_buttons(self):
        """Hide the welcome label, Host and Join buttons after game starts."""
        self.host_button.pack_forget()
        self.join_button.pack_forget()
        self.welcome_label.pack_forget()

    def on_close(self):
        """Terminate the game server when closing the window."""
        print("Closing the game...")
        self.root.quit()  # Close the window
        # Here you can add logic to stop the server or close any active connections if necessary
        # For example, if you are running a server, you should properly stop it before quitting

if __name__ == "__main__":
  game=Game()