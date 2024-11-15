import unittest
from unittest.mock import AsyncMock, patch
import asyncio
import socket
from network import P2PNetwork



#still working on these as i keep geeting error for method returning none
class TestP2PNetwork(unittest.TestCase):
    @patch('asyncio.start_server', new_callable=AsyncMock)
    @patch('asyncio.open_connection', new_callable=AsyncMock)
    async def test_host_and_connect_localhost_8888(self, mock_open_connection, mock_start_server):
        network = P2PNetwork(host='localhost', port=8888)
        await network.start_host()
        mock_start_server.assert_called_once_with(network.handle_client, 'localhost', 8888)
        await network.connect_to_host('localhost', 8888)
        mock_open_connection.assert_called_once_with('localhost', 8888)

    @patch('asyncio.start_server', new_callable=AsyncMock)
    @patch('asyncio.open_connection', new_callable=AsyncMock)
    async def test_host_and_connect_local_ip_8080(self, mock_open_connection, mock_start_server):
        network = P2PNetwork(host='127.0.0.1', port=8080)
        await network.start_host()
        mock_start_server.assert_called_once_with(network.handle_client, '127.0.0.1', 8080)
        await network.connect_to_host('127.0.0.1', 8080)
        mock_open_connection.assert_called_once_with('127.0.0.1', 8080)

    @patch('asyncio.start_server', new_callable=AsyncMock)
    @patch('asyncio.open_connection', new_callable=AsyncMock)
    async def test_host_and_connect_dynamic_port(self, mock_open_connection, mock_start_server):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('localhost', 0))
            dynamic_port = s.getsockname()[1]
        network = P2PNetwork(host='localhost', port=dynamic_port)
        await network.start_host()
        mock_start_server.assert_called_once_with(network.handle_client, 'localhost', dynamic_port)
        await network.connect_to_host('localhost', dynamic_port)
        mock_open_connection.assert_called_once_with('localhost', dynamic_port)

if __name__ == '__main__':
    unittest.main()
