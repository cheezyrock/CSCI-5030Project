import unittest
from unittest.mock import Mock
from DecisionPoints import Player, DecisionPointsUI, GameIntegration

class RunDPTests(unittest.TestCase):
    def setUp(self):
        print("Setting up tests...")
        
        self.player1 = Player(1)
        self.player1.decision_points = 6
        
        self.player2 = Player(2)
        self.player2.decision_points = 2
        
        self.ui = DecisionPointsUI([self.player1, self.player2])
        self.decision_manager = Mock()
        self.game_integration = GameIntegration([self.player1, self.player2], self.decision_manager)
        
    def test_reset_dp(self):
        print("Testing reset_dp...")
        self.player1.reset_dp()
        self.assertEqual(self.player1.decision_points, 0, "Decision points should be reset to 0.")
        
    def test_award_dp(self):
        print("Testing award_dp...")
        self.player1.award_dp()
        self.assertEqual(self.player1.decision_points, 7, "Decision points should be 7 after award.")
        
    def test_spend_dp(self):
        print("Testing spend_dp...")
        success = self.player1.spend_dp(3)
        self.assertTrue(success, "Should be able to spend 3 points.")
        self.assertEqual(self.player1.decision_points, 3, "Decision points should be 3 after spending.")

        success = self.player1.spend_dp(7)
        self.assertFalse(success, "Should not be able to spend more points than available.")

    def test_ui_dp(self):
        print("Testing ui_dp...")
        self.ui.display_dp()


if __name__ == "__main__":
    unittest.main()
