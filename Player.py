
class Player:
    def __init__(self, name: str):
        self.name = name
        self.decisions = []  
        self.decisionPoints = 0  

    def addDecision(self, decision: 'Decision'):
        from Decision import Decision
        self.decisions.append(decision)

    def getDecisions(self):
        return self.decisions

    def awardDecisionPoints(self):
        self.decisionPoints += 1

    def getDecisionPoints(self):
    
        return self.decisionPoints



