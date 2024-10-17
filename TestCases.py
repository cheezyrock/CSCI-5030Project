import unittest
from unittest import mock
from DecisionPoints import Player, DecisionPointsUI, GameIntegration

class RunDPTests(unittest.TestCase):
    def setup(self):
        self.player = Player(1)
        self.player.decision.points = 5
        self.ui = DecisionPointsUI([self.player])
        self.decision_manager = mock()
        #self.decision_manager = DecisionManager()     # replace with actual DM
        #self.game_integration = GameIntegration([self.player], decision_manager)
        
    def test_reset_dp(self):
        self.player.reset_dp()
        self.assertEqual(self.player.decision_points, 0, "Decision points should be reset to 0.")
        
    def test_award_dp(self):
        self.player.award_dp()
        self.assertEqual(self.player.decision_points, 6, "Decision points should be 6 after award.")
        
    def test_spend_dp(self):
        success = self.player.spend_dp(3)
        self.assertTrue(success, "Should be able to spend 3 points.")
        self.assertEqual(self.player.decision_points, 2, "Decision points should be 2 after spending.")

        success = self.player.spend_dp(5)
        self.assertFalse(success, "Should not be able to spend more points than available.")

    def test_ui_dp(self):
        self.ui.display_dp()
        
        
if __name__ == "__main__":
    unittest.main()