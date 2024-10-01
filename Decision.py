class Decision:
    def __init__(self, playerChoice: str, nextStory: 'Narrative'):
        self.playerChoice = playerChoice
        self.nextStory = nextStory
        
    def getPlayerChoice(self):
        
        return self.playerChoice
    
    def getNextStory(self):
        from Narrative import Narrative
        return self.nextStory
    
    def setNextStory(self, nextStory: 'Narrative'):
        self.nextStory = nextStory