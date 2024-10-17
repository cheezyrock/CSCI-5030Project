class Player:
    def __init__(self, player_id):
        self.player_id = player_id
        self.decision_points = 0
        self.last_decision = None
        
    def record_decision(self, decision):
        self.last_decision = decision
        
    def reset_dp(self):
        self.decision_points = 0
        
    # if GroupDecision != player's decision, then award_dp
    def award_dp(self):
        self.decision_points += 1
    
    # confirms required num of decision points is met and spends them
    def spend_dp(self, required_points):
        if self.decision_points >= required_points:
            self.decision_points -= required_points
            return True
        return False
        
    
class DecisionPointsUI:
    def __init__(self, players):
        self.players = players
        
    def display_dp(self):
        print ("Current Decision Points:")
        for player in self.players:
            print(f"Player {player.player_id}'s Decision Points: {player.decision_points}")
            
    def update_dp(self,player):
        print(f"Player {player.player_id}'s Decision Points Updated: {player.decision_points}")
        

class GameIntegration:
    def __init__(self, players, decision_manager):
        self.players = players
        self.decision_manager = decision_manager
        
    def handle_group_decision(self, group_decision):
        #calls the decision manager method to handle decision
        self.decision_manager.override_decision(group_decision)
        
        # Award points to players basde on their last decision
        for player in self.players:
            if player.last_decision != group_decision:
                player.award_dp()
                
    def spend_decision_points(self, player_id, required_points):
        for p in self.players:              # look through player list
            if p.player_id == player_id:
                player = p                  # player found is assigned
                break                       # exit
        if player:
            if player.spend_dp(required_points):
                print(f"Player {player.player_id}'s Decision Points Updated: {player.decision_points}")
            else:
                print(f"Player {player.player_id} does not have enough decision points.")
        else:
            print(f"Player {player_id} not found.")