import asyncio

class P2PNetwork:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.peers = []

    async def start_host(self):
        """Start a game server"""
        server = await asyncio.start_server(self.handle_client, self.host, self.port)
        async with server:
            print(f"Hosting game on {self.host}:{self.port}")
            await server.serve_forever()

    async def handle_client(self, reader, writer):
        """Handle incoming client connection"""
        self.peers.append((reader, writer))
        print("Client connected")

    async def discover_games(self):
        """Discover available games on the network"""
        # Placeholder function - In real use, implement broadcast or scanning mechanism
        available_games = [("localhost", 8888)]  # Example game list
        return available_games

    async def connect_to_host(self, host, port):
        """Connect to an existing game"""
        reader, writer = await asyncio.open_connection(host, port)
        self.peers.append((reader, writer))
        print(f"Connected to game at {host}:{port}")
