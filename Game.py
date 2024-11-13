import tkinter as tk
from tkinter import messagebox
from story_builder import StoryBuilder
from image_handler import ImageHandler
import Audio
import asyncio
import threading
import socket

class Game:
    def __init__(self):
        self.story = StoryBuilder.create_story()
        self.current_node = self.story

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
            for i, choice in enumerate(self.current_node.choices):
                button = tk.Button(self.button_frame, text=choice.text, command=lambda index=i: self.make_choice(index))
                button.pack(pady=5)
        else:
            messagebox.showinfo("Game Over", self.current_node.text)
            self.root.quit()

    def make_choice(self, index):
        """Update the game state based on the player's choice."""
        self.current_node = self.current_node.choices[index]
        Audio.SFX.playSFX("ButtonPress.mp3")
        self.display_choices()

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
            reader, writer = await asyncio.wait_for( 
                asyncio.open_connection(host, port), timeout=10)
            game_intro = await reader.read(100)  # Receive initial story data
            self.story_text.set(game_intro.decode())
            self.display_choices()  # Show the story after joining
        except ConnectionRefusedError:
            messagebox.showerror("Connection Error","No game hosted at the provided IP address.")
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

#if __name__ == "__main__":
 #   game = Game()
