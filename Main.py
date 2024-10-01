from StoryNode import StoryNode
from Game import Game
from Player import Player
from GraphicsUtilities import GraphicsUtilities

# Create Story Nodes
story1 = StoryNode("You enter a dark room with two doors.", 
                   [("Take the left door", None), ("Take the right door", None)])
story2 = StoryNode("You encounter a dragon!", 
                   [("Fight the dragon", None), ("Run away", None)])

# Initialize Player and Game
player = Player("Player1")
game = Game(player, [story1, story2])

# Start the UI
game_ui = GraphicsUtilities(game)
game_ui.run()

if __name__ == "__main__":
    main()
