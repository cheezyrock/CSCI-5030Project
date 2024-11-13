import os
import json
import asyncio
from pathlib import Path
from typing import List

from GameAssetVerification import generate_manifest

# Directory for storing files and manifest
gameAssetsDirectory = os.path.join(os.getcwd(), "/GameAssets")
localManifest = os.path.join(gameAssetsDirectory, "/manifest.json")

class P2PNetwork:

    def __init__(self, host: str, port: int):

        self.host = host
        self.port = port
        self.peers: list[tuple[asyncio.StreamReader, asyncio.StreamWriter]] = []

    async def start_host(self):
        
        server = await asyncio.start_server(self.handle_client, self.host, self.port)
        async with server:
            print(f"Hosting game on {self.host}:{self.port}")
            await server.serve_forever()

    async def handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        
        self.peers.append((reader, writer))
        print("Client connected")
        await self.SynchronizeFiles(reader, writer)

    async def discover_games(self) -> List[tuple[str, int]]:
        
        available_games = [("localhost", 8888)] 
        return available_games

    async def connect_to_host(self, host: str, port: int):
        
        try:
            reader, writer = await asyncio.open_connection(host, port)
            self.peers.append((reader, writer))
            
            await self.SynchronizeFiles(reader, writer)

        except ConnectionRefusedError:
            print(f"Failed to connect to {host}:{port} - No game hosted.")

        except Exception as e:
            print(f"Failed to connect to {host}:{port} - {e}")


    async def SynchronizeFiles(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        
        localManifest = self.LoadLocalManfest()
        remoteManifest = await self.ReceiveManifest(reader)
        
        for fileName, fileSize in remoteManifest.items():
            filePath = os.path.join(gameAssetsDirectory, fileName)
            if fileName not in localManifest or localManifest[fileName] != fileSize:
                await self.DownloadFile(fileName, reader, writer)
        
        for fileName, local_size in localManifest.items():
            if fileName not in remoteManifest or remoteManifest[fileName] != local_size:
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

    
    def GenerateManifest(self, directory: str):
        
        manifest = {}
        for filePath in Path(directory).rglob('*'):
            if filePath.is_file():
                file_size = os.path.getsize(filePath)
                manifest[filePath.relative_to(directory).as_posix()] = str(file_size)

        self.SaveLocalManifest()
        return manifest


    def LoadLocalManfest(self) -> dict:
        
        if os.path.exists(localManifest):
            with open(localManifest, 'r') as f:
                return json.load(f)
            
        return self.GenerateManifest()


    def SaveLocalManifest(manifest: dict):
        
        with open(localManifest, 'w') as f:
            json.dump(manifest, f, indent=4)

