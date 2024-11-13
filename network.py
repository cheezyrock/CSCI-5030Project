import os
import json
import asyncio
import threading
from tkinter import messagebox
import socket
from pathlib import Path

# Directory for storing files and manifest
gameAssetsDirectory = os.path.join(os.path.split(os.path.abspath(__file__))[0], "GameAssets")
localManifest = os.path.join(gameAssetsDirectory, "manifest.json")

class P2PNetwork:
    def __init__(self):
        self.peers: list[tuple[asyncio.StreamReader, asyncio.StreamWriter]] = []


    # P2P Networking Methods
    def host_game(self):
        """Host a new game and start listening for incoming connections."""
        threading.Thread(target=asyncio.run, args=(self.start_host_server(),)).start()
        print("Hosting game...")
        if not os.path.exists(localManifest):
            self.GenerateManifest()
        
        self.LoadLocalManfest()

    def start_game(self):
        """Start the game logic for the host after hosting the game."""
        self.play()  # Start the game loop for the host

    async def start_host_server(self):
        """Start a server that allows players to connect."""
        server = await asyncio.start_server(self.handle_client, '192.168.1.85', 8888)
        async with server:
            print(f"Hosting game on localhost:8888")
            await server.serve_forever()

    async def handle_client(self, reader, writer):
        """Handle incoming client connections and share game data."""
        self.peers.append((reader,writer))
        print("A player has connected.")
        # Send the initial game state to the connected player
        await self.SynchronizeFiles(reader, writer, True)

        writer.write(self.current_node.text.encode())
        await writer.drain()

    def join_game(self, peer_ip):
        """Allow the user to input a host's IP and connect to an existing game."""
        if peer_ip:
            threading.Thread(target=asyncio.run, args=(self.connect_to_host(peer_ip, 8888),)).start()
        else:
            messagebox.showerror("Error", "Please enter a valid IP address.")

    async def connect_to_host(self, host, port):
        """Connect to an existing game hosted by another player."""
        try:
            reader, writer = await asyncio.wait_for( 
                asyncio.open_connection(host, port), timeout=10)
            
            await self.SynchronizeFiles(reader, writer)

            game_intro = await reader.read(100)  # Receive initial story data
            self.story_text.set(game_intro.decode())
            self.display_choices()  # Show the story after joining
        except ConnectionRefusedError:
            messagebox.showerror("Connection Error","No game hosted at the provided IP address.")
        except Exception as e:
            messagebox.showerror("Connection Error", f"Failed to connect to the game: {e}")

    


    async def SynchronizeFiles(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter, isHost: bool = False):
        
        lm = self.LoadLocalManfest()

        if isHost:
            await self.SendManifest(writer, lm)

            remote_manifest = await self.ReceiveManifest(reader)

        else:
            remote_manifest = await self.ReceiveManifest(reader)

            await self.SendManifest(writer, lm) 
        
        await self.TransferFiles(lm, rm, reader, writer)

    async def TransferFiles (self, lm, rm, reader, writer):

        for fileName, fileSize in rm.items():
            filePath = os.path.join(gameAssetsDirectory, fileName)
            if fileName not in lm or lm[fileName] != fileSize:
                await self.DownloadFile(fileName, reader, writer)
        
        for fileName, local_size in lm.items():
            if fileName not in rm or rm[fileName] != local_size:
                await self.UploadFile(fileName, reader, writer)


    async def DownloadFile(self, fileName: str, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        
        filePath = os.path.join(gameAssetsDirectory, fileName)
        writer.write(f"DOWNLOAD {fileName}".encode())
        await writer.drain()

        file_data = await reader.read()
        with open(filePath, 'wb') as f:
            f.write(file_data)


    async def UploadFile(self, fileName: str, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        
        filePath = os.path.join(gameAssetsDirectory, fileName)
        with open(filePath, 'rb') as f:
            file_data = f.read()

        writer.write(f"UPLOAD {fileName}".encode())
        await writer.drain()

        writer.write(file_data)
        await writer.drain()
        

    async def ReceiveManifest(self, reader: asyncio.StreamReader):
        
        data = await reader.read(1024)
        manifest = json.loads(data.decode())
        return manifest


    async def SendManifest(self, writer: asyncio.StreamWriter, manifest):

        writer.write(json.dumps(manifest).encode())
        await writer.drain()

    
    def GenerateManifest(self) -> list:
        
        manifest = {}
        for filePath in Path(gameAssetsDirectory).rglob('*'):
            if filePath.is_file():
                file_size = os.path.getsize(filePath)
                manifest[filePath.relative_to(gameAssetsDirectory).as_posix()] = str(file_size)

        self.SaveLocalManifest(manifest)
        return manifest


    def LoadLocalManfest(self) -> list:
        
        if os.path.exists(localManifest):
            with open(localManifest, 'r') as man:
                return json.load(man)
            
        return {}


    def SaveLocalManifest(self, manifest: list):
        
        with open(localManifest, 'w') as man:
            json.dump(manifest, man, indent=4)

