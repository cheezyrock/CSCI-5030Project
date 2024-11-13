import asyncio

class P2PNetwork:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.peers: list[tuple[asyncio.StreamReader, asyncio.StreamWriter]] = []

    async def start_host(self):
        """Start a game server and listen for incoming connections on the specified host and port."""
        server = await asyncio.start_server(self.handle_client, self.host, self.port)
        async with server:
            print(f"Hosting game on {self.host}:{self.port}")
            await server.serve_forever()

    async def handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        """Handle incoming client connection by adding them to the peer list."""
        self.peers.append((reader, writer))
        print("Client connected")

    async def discover_games(self) -> list[tuple[str, int]]:
        """Discover available games on the network by returning a static list of example games."""
        available_games = [("localhost", 8888)]  # Example game list
        return available_games

    async def connect_to_host(self, host: str, port: int):
        """Attempt to connect to an existing game and add it to peers list."""
        try:
            reader, writer = await asyncio.open_connection(host, port)
            self.peers.append((reader, writer))
            print(f"Connected to game at {host}:{port}")
        except ConnectionRefusedError:
            print(f"Failed to connect to {host}:{port} - No game hosted.")
        except Exception as e:
            print(f"Failed to connect to {host}:{port} - {e}")
