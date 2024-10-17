from story_node import StoryNode

class StoryBuilder:
    @staticmethod
    def create_story():
        # End node
        end_node = StoryNode("Your adventure ends here. Thanks for playing!", [] ,"adventure-ends.jpeg")

        # Story nodes
        choice_6 = StoryNode("You are at the edge of the forest. What do you do?", [
            StoryNode("Go back", [end_node], "turn-back-forest.jpeg"),
            StoryNode("Jump from the edge", [end_node], "jump-forest.jpeg"),
        ], "forest-edge.jpeg")

        choice_5 = StoryNode("A wise man offers potions. Which do you choose?", [
            StoryNode("Strength potion.", [choice_6], "strength-potion.jpeg"),
            StoryNode("Wisdom potion.", [choice_6], "wisdom.jpeg"),
            StoryNode("Invisibility potion.", [choice_6], "invisibility.jpeg")
        ], "man-with-potions.jpeg")

        choice_4 = StoryNode("A fork in the road. Go left or right?", [
            StoryNode("Left to the mountains.", [choice_5], "mountain-road.jpeg"),
            StoryNode("Right to the valley.", [choice_5], "right-valley.jpeg"),
            StoryNode("Go back.", [end_node], "turn-back-forest.jpeg")
        ], "forked-road.jpeg")

        choice_3 = StoryNode("A dragon appears! What do you do?", [
            StoryNode("Fight!", [choice_4], "fighting-dragon.jpeg"),
            StoryNode("Flee.", [choice_4], "running-from-dragon.jpeg"),
            StoryNode("Negotiate.", [choice_4], "talking-with-dragon.jpeg")
        ], "dragon.jpeg")

        choice_2 = StoryNode("You find a map. What now?", [
            StoryNode("Follow it.", [choice_3],"map-follow.png"),
            StoryNode("Ignore it.", [choice_3],"map-ignore.png"),
            StoryNode("Burn it.", [end_node],"map-burn.png" )
        ],"map.jpeg")

        choice_1 = StoryNode("You awaken in a strange land. What next?", [
            StoryNode("Explore.", [choice_2],"exploring.png"),
            StoryNode("Seek help.", [choice_2],"seek-help.png"),
            StoryNode("Camp.", [end_node],"camping.png")
        ],"start-image.png")

        # Starting point
        start_node = StoryNode("You find yourself in a lush, unfamiliar land.", [
            choice_1,
        ], "lush-garden.jpeg")

        return start_node
