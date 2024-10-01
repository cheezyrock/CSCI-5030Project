class StoryNode:
    def __init__(self, narrative, choices):
        self.narrative = narrative
        self.choices = choices  # List of tuples (choice_text, next_node)

    def get_narrative(self):
        return self.narrative

    def get_choices(self):
        return self.choices