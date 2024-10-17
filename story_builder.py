from story_node import StoryNode

class StoryBuilder:
    @staticmethod
    def create_story():
        # End node
        end_node = StoryNode("Your adventure ends here. Thanks for playing!", [] ,"./Images/advensure-ends.jpeg")

        # Story nodes
        choice_6 = StoryNode("You are at the edge of the forest. What do you do?", [
            StoryNode("Go back", [end_node], "./Images/turn-back-forest.jpeg"),
            StoryNode("Jump from the edge", [end_node], "./Images/jump-forest.jpeg"),
        ], "./Images/forest-edge.jpeg")

        choice_5 = StoryNode("A wise man offers potions. Which do you choose?", [
            StoryNode("Strength potion.", [choice_6], "./Images/strength-potion.jpeg"),
            StoryNode("Wisdom potion.", [choice_6], "./Images/wisdom.jpeg"),
            StoryNode("Invisibility potion.", [choice_6], "./Images/invisibility.jpeg")
        ], "./Images/man-with-potions.jpeg")

        choice_4 = StoryNode("A fork in the road. Go left or right?", [
            StoryNode("Left to the mountains.", [choice_5], "./Images/mountain-road.jpeg"),
            StoryNode("Right to the valley.", [choice_5], "./Images/right-valley.jpeg"),
            StoryNode("Go back.", [end_node], "./Images/turn-back-forest.jpeg")
        ], "./Images/forked-road.jpeg")

        choice_3 = StoryNode("A dragon appears! What do you do?", [
            StoryNode("Fight!", [choice_4], "./Images/fighting-dragon.jpeg"),
            StoryNode("Flee.", [choice_4], "./Images/running-from-dragon.jpeg"),
            StoryNode("Negotiate.", [choice_4], "./Images/talking-with-dragon.jpeg")
        ], "./Images/dragon.jpeg")

        choice_2 = StoryNode("You find a map. What now?", [
            StoryNode("Follow it.", [choice_3],"./Images/map-follow.png"),
            StoryNode("Ignore it.", [choice_3],"./Images/map-ignore.png"),
            StoryNode("Burn it.", [end_node],"./Images/map-burn.png" )
        ],"./Images/map.jpeg")

        choice_1 = StoryNode("You awaken in a strange land. What next?", [
            StoryNode("Explore.", [choice_2],"./Images/exploring.png"),
            StoryNode("Seek help.", [choice_2],"./Images/seek-help.png"),
            StoryNode("Camp.", [end_node],"./Images/camping.png")
        ],"./Images/start-image.png")

        # Starting point
        start_node = StoryNode("You find yourself in a lush, unfamiliar land.", [
            choice_1,
        ], "./Images/lush-garden.jpeg")

        return start_node
