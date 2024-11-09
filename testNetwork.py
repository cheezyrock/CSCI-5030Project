import asyncio
import threading
import unittest
import time
from unittest.mock import patch
from Game import Game

class TestGame(unittest.TestCase):

    @patch("Game.Game.start_host_server", autospec=True)
    def test_host_game(self, mock_start_host_server):
        game = Game()
        game.host_game()
        time.sleep(0.1)
        mock_start_host_server.assert_called()
        print("Test passed: start_host_server was called in host_game.")

if __name__ == "__main__":
    unittest.main()
