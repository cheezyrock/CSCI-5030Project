import tkinter as tk
from tkinter import messagebox
from story_builder import StoryBuilder
from image_handler import ImageHandler
import Audio
import asyncio
import threading
import socket
from DecisionPoints import Player, DecisionPointsUI, GameIntegration

class Game:
    def __init__(self):
        self.story = StoryBuilder.create_story()
        self.current_node = self.story
        self.players = [Player(player_id=i) for i in range(1, 3)]  # Example: two players
        self.decision_manager = GameIntegration(self.players, DecisionPointsUI(self.players))
        self.current_player_index = 0  # Player 1 starts
        
        # Set up the main window
        self.root = tk.Tk()
        self.root.title("Interactive Story Game")

        # Register the close event to ensure proper termination
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.story_text = tk.StringVar()

        # Welcome message
        self.welcome_label = tk.Label(self.root, text="Welcome to the Interactive Story Game!", font=('Helvetica', 14), pady=20)
        self.welcome_label.pack()

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

        # Track connected players
        self.connected_players = []

        self.root.mainloop()

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
            current_player = self.players[self.current_player_index]  # Gets current player
            for i, choice in enumerate(self.current_node.choices):
                button = tk.Button(self.button_frame, text=choice.text, command=lambda index=i: self.make_choice(index, current_player.player_id))
                button.pack(pady=5)
        else:
            messagebox.showinfo("Game Over", self.current_node.text)
            self.root.quit()

    def make_choice(self, index, player_id):
        """Update the game state based on the player's choice."""
        player = next((p for p in self.players if p.player_id == player_id), None)
        if player:
            player.record_decision(index)
        else:
            print(f"player with id {player_id} not found")
            return
        self.current_node = self.current_node.choices[index]
        Audio.SFX.playSFX("Button.wav")
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