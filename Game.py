class Game:
    def __init__(self,player, story_nodes):
        self.player = player
        self.story_nodes = story_nodes
        self.current_node = story_nodes[0] 

    def get_current_narrative(self):
        return self.current_node.get_narrative()

    def get_current_choices(self):
        return self.current_node.get_choices()

    def make_choice(self, choice_index):
        """Make a choice, update the current story node"""
        next_node = self.current_node.get_choices()[choice_index][1]
        self.current_node = next_node

    def is_game_over(self):
        return len(self.current_node.get_choices()) == 0  
