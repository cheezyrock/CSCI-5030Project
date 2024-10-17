from story_node import StoryNode

class StoryBuilder:
    @staticmethod
    def create_story():
        # End node
        end_node = StoryNode("Your adventure ends here. Thanks for playing!", [] ,"./GameAssets/Images/adventure-ends.jpeg")

        # Story nodes
        choice_6 = StoryNode("You are at the edge of the forest. What do you do?", [
            StoryNode("Go back", [end_node], "./GameAssets/Images/turn-back-forest.jpeg"),
            StoryNode("Jump from the edge", [end_node], "./GameAssets/Images/jump-forest.jpeg"),
        ], "./GameAssets/Images/forest-edge.jpeg")

        choice_5 = StoryNode("A wise man offers potions. Which do you choose?", [
            StoryNode("Strength potion.", [choice_6], "./GameAssets/Images/strength-potion.jpeg"),
            StoryNode("Wisdom potion.", [choice_6], "./GameAssets/Images/wisdom.jpeg"),
            StoryNode("Invisibility potion.", [choice_6], "./GameAssets/Images/invisibility.jpeg")
        ], "./GameAssets/Images/man-with-potions.jpeg")

        choice_4 = StoryNode("A fork in the road. Go left or right?", [
            StoryNode("Left to the mountains.", [choice_5], "./GameAssets/Images/mountain-road.jpeg"),
            StoryNode("Right to the valley.", [choice_5], "./GameAssets/Images/right-valley.jpeg"),
            StoryNode("Go back.", [end_node], "./GameAssets/Images/turn-back-forest.jpeg")
        ], "./GameAssets/Images/forked-road.jpeg")

        choice_3 = StoryNode("A dragon appears! What do you do?", [
            StoryNode("Fight!", [choice_4], "./GameAssets/Images/fighting-dragon.jpeg"),
            StoryNode("Flee.", [choice_4], "./GameAssets/Images/running-from-dragon.jpeg"),
            StoryNode("Negotiate.", [choice_4], "./GameAssets/Images/talking-with-dragon.jpeg")
        ], "./GameAssets/Images/dragon.jpeg")

        choice_2 = StoryNode("You find a map. What now?", [
            StoryNode("Follow it.", [choice_3],"./GameAssets/Images/map-follow.png"),
            StoryNode("Ignore it.", [choice_3],"./GameAssets/Images/map-ignore.png"),
            StoryNode("Burn it.", [end_node],"./GameAssets/Images/map-burn.png" )
        ],"./GameAssets/Images/map.jpeg")

        choice_1 = StoryNode("You awaken in a strange land. What next?", [
            StoryNode("Explore.", [choice_2],"./GameAssets/Images/exploring.png"),
            StoryNode("Seek help.", [choice_2],"./GameAssets/Images/seek-help.png"),
            StoryNode("Camp.", [end_node],"./GameAssets/Images/camping.png")
        ],"./GameAssets/Images/start-image.png")

        # Starting point
        start_node = StoryNode("You find yourself in a lush, unfamiliar land.", [
            choice_1,
        ], "./GameAssets/Images/lush-garden.jpeg")

        return start_node
