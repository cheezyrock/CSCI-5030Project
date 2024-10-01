class Narrative:
    def __init__(self, narrativeText: str):
        self.story = narrativeText
        self.choices = []
        
    def getStory(self):
        
        return self.story
    
    def getChoices(self):
        return self.choices
    
    def addChoice(self, playerDecision: 'Decision'):
        from Decision import Decision
        self.choices.append(playerDecision)
        
    def removeChoice(self, playerDecision: 'Decision'):
        if playerDecision in self.choices:
            self.choices.remove(playerDecision)
        else:
            raise ValueError("This decision is not found in the list of choices")
        
        