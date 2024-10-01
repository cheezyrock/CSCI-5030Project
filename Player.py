
class Player:
    def __init__(self, name: str):
        self.name = name
        self.decisions = []  
        self.decisionPoints = 0 
    
    def addDecision(self, storyNode: 'StoryNode'):
       # from Decision import Decision
        self.decisions.append(storyNode)
        
    def getDecisions(self):
        return self.decisions

    def awardDecisionPoints(self):
        self.decisionPoints += 1

    def getDecisionPoints(self):
    
        return self.decisionPoints



