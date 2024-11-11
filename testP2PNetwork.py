import asyncio
import unittest
from unittest.mock import AsyncMock, patch
from network import P2PNetwork


class TestP2PNetwork(unittest.TestCase):
    def setUp(self):
        self.host = 'localhost'
        self.port = 8888
        self.network = P2PNetwork(self.host, self.port)

#testcase for starting server successfully
    @patch('asyncio.start_server', new_callable=AsyncMock)
    def test_start_host(self, mock_start_server):
        # Mock the server to prevent actual server start
        mock_server = AsyncMock()
        mock_start_server.return_value = mock_server
        asyncio.run(self.network.start_host())
        mock_start_server.assert_called_once_with(self.network.handle_client, self.host, self.port)
        mock_server.serve_forever.assert_called_once()

#test for add players to list of peers list
    def test_handle_players(self):
        reader = AsyncMock()
        writer = AsyncMock()
        asyncio.run(self.network.handle_client(reader, writer))
        self.assertEqual(len(self.network.peers), 1)
        self.assertEqual(self.network.peers[0], (reader, writer))

#test to ensure connect to host works
    @patch('asyncio.open_connection', new_callable=AsyncMock)
    def test_connect_to_host_success(self, mock_open_connection):
        reader = AsyncMock()
        writer = AsyncMock()
        mock_open_connection.return_value = (reader, writer)
        asyncio.run(self.network.connect_to_host(self.host, self.port))
        self.assertEqual(len(self.network.peers), 1)
        self.assertEqual(self.network.peers[0], (reader, writer))
        mock_open_connection.assert_called_once_with(self.host, self.port)

#test to ensure connection failure is handled
    @patch('asyncio.open_connection', new_callable=AsyncMock)
    def test_connect_to_host_failure(self, mock_open_connection):
        mock_open_connection.side_effect = Exception("Connection failed")
        asyncio.run(self.network.connect_to_host(self.host, self.port))
        self.assertEqual(len(self.network.peers), 0)
        mock_open_connection.assert_called_once_with(self.host, self.port)

#test for discovering f=games hosted
    def test_discover_games(self):
        games = asyncio.run(self.network.discover_games())
        self.assertEqual(games, [("localhost", 8888)])


if __name__ == '__main__':
    unittest.main()


