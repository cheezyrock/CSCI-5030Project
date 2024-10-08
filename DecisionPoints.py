class ResetDecisionPoints:
    def reset_dp(self, num_dpoints):
        self.decision_points = 0
        
# if GroupDecision != player's decision, then award_dp
class AwardDecisionPoints:
    def award_dp(self, num_dpoints):
        self.decision_points += 1

class SpendDecisionPoints:
    def spend_dp(self, num_dpoints):
        self.decision_points -= 1
        
'''class DecisionPointsUI:
    def ui_dp():
        print(f"Decision Points: {decision_points}")
            # display current decision points'''
class RunDPTests:
    def test_reset_dp():
        # insert test
    def test_award_dp():
        # insert test
    def test_spend_dp():
        # insert test
    def test_ui_dp:
        # insert test